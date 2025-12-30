#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DataSource Hub - URL Verification Script
Verifies that all URLs in data source files are accessible
"""

import json
import sys
import time
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from urllib.parse import urlparse

try:
    import requests
    from requests.adapters import HTTPAdapter
    from requests.packages.urllib3.util.retry import Retry
except ImportError:
    print("❌ Error: requests package not installed")
    print("Install with: pip install requests")
    sys.exit(1)


class URLVerifier:
    """Verifies URLs from data source metadata files"""

    def __init__(self, timeout: int = 10, max_retries: int = 3):
        """
        Initialize URL verifier

        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.timeout = timeout
        self.max_retries = max_retries

        # Setup session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Use standard browser User-Agent to avoid being blocked
        # Many sites block non-browser user agents
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        })

    def extract_urls(self, data: Dict) -> Dict[str, str]:
        """
        Extract all URLs from data source JSON

        Returns:
            Dictionary mapping field names to URLs
        """
        urls = {}

        # Primary URL (required)
        primary_url = data.get('access', {}).get('primary_url')
        if primary_url:
            urls['primary_url'] = primary_url

        # Organization website
        org_website = data.get('organization', {}).get('website')
        if org_website:
            urls['organization.website'] = org_website

        # API documentation
        api_docs = data.get('access', {}).get('api', {}).get('documentation')
        if api_docs:
            urls['access.api.documentation'] = api_docs

        # Support URL
        support_url = data.get('contact', {}).get('support_url')
        if support_url:
            urls['contact.support_url'] = support_url

        return urls

    def verify_url(self, url: str, field_name: str) -> Tuple[bool, int, str]:
        """
        Verify a single URL

        Returns:
            (success, status_code, message)
        """
        # Basic URL validation
        try:
            parsed = urlparse(url)
            if not all([parsed.scheme, parsed.netloc]):
                return False, 0, "Invalid URL format"

            if parsed.scheme not in ['http', 'https']:
                return False, 0, f"Unsupported scheme: {parsed.scheme}"
        except Exception as e:
            return False, 0, f"URL parsing error: {e}"

        # Try to access the URL
        response = None
        head_failed = False

        # Try HEAD request first (faster)
        try:
            response = self.session.head(
                url,
                timeout=self.timeout,
                allow_redirects=True
            )

            # If HEAD returns error status codes, try GET
            # Some sites block HEAD requests but allow GET
            if response.status_code >= 400 or response.status_code == 405:
                head_failed = True
        except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout):
            # HEAD request timed out, will try GET
            head_failed = True
        except Exception:
            # Other errors with HEAD, will try GET
            head_failed = True

        # If HEAD failed or returned error, try GET
        if head_failed or response is None:
            try:
                response = self.session.get(
                    url,
                    timeout=self.timeout,
                    allow_redirects=True
                )
            except requests.exceptions.SSLError as e:
                # SSL error encountered, try HTTP version
                if url.startswith('https://'):
                    http_url = url.replace('https://', 'http://', 1)
                    try:
                        response = self.session.get(
                            http_url,
                            timeout=self.timeout,
                            allow_redirects=True
                        )
                        # If HTTP works, return success with note
                        if response.status_code == 200:
                            return True, response.status_code, f"OK (HTTPS failed, used HTTP: {http_url})"
                    except Exception:
                        pass  # HTTP also failed, return original SSL error
                return False, 0, f"SSL error: {str(e)[:100]}"
            except requests.exceptions.Timeout:
                return False, 0, f"Timeout after {self.timeout}s"
            except requests.exceptions.ConnectionError:
                return False, 0, "Connection error (host unreachable)"
            except requests.exceptions.TooManyRedirects:
                return False, 0, "Too many redirects"
            except requests.exceptions.RequestException as e:
                return False, 0, f"Request error: {str(e)[:100]}"
            except Exception as e:
                return False, 0, f"Unexpected error: {str(e)[:100]}"

        # Analyze response
        if response is None:
            return False, 0, "No response received"

        status_code = response.status_code

        # Success codes
        if 200 <= status_code < 300:
            return True, status_code, "OK"

        # Redirection codes (should be followed by allow_redirects)
        elif 300 <= status_code < 400:
            return True, status_code, f"Redirect to {response.headers.get('Location', 'unknown')}"

        # Client errors
        elif 400 <= status_code < 500:
            if status_code == 401:
                # Authentication required might be expected
                return True, status_code, "Authentication required (expected for some sources)"
            elif status_code == 403:
                return False, status_code, "Forbidden (possible anti-bot protection)"
            elif status_code == 404:
                return False, status_code, "Not Found"
            else:
                return False, status_code, f"Client error"

        # Server errors
        else:
            return False, status_code, "Server error"

    def verify_file(self, file_path: Path, verbose: bool = True) -> Tuple[bool, Dict]:
        """
        Verify all URLs in a data source file

        Returns:
            (all_passed, results)
        """
        if verbose:
            print(f"\n{'='*70}")
            print(f"Verifying URLs in: {file_path}")
            print(f"{'='*70}\n")

        # Load JSON file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON: {e}")
            return False, {'error': f'Invalid JSON: {e}'}
        except Exception as e:
            print(f"❌ Error: Failed to read file: {e}")
            return False, {'error': f'Failed to read file: {e}'}

        # Extract URLs
        urls = self.extract_urls(data)

        if not urls:
            print("⚠️  Warning: No URLs found in file")
            return True, {'urls': {}}

        # Verify each URL
        all_passed = True
        results = {'urls': {}}

        for field_name, url in urls.items():
            if verbose:
                print(f"Checking {field_name}:")
                print(f"  URL: {url}")

            # Add small delay between requests to be respectful
            if field_name != list(urls.keys())[0]:
                time.sleep(0.5)

            success, status_code, message = self.verify_url(url, field_name)

            results['urls'][field_name] = {
                'url': url,
                'success': success,
                'status_code': status_code,
                'message': message
            }

            if success:
                if verbose:
                    status_display = f"{status_code}" if status_code > 0 else "N/A"
                    print(f"  ✅ Status code: {status_display} - {message}\n")
            else:
                all_passed = False
                if verbose:
                    status_display = f"{status_code}" if status_code > 0 else "N/A"
                    print(f"  ❌ Status code: {status_display} - {message}\n")

        # Summary
        if verbose:
            print(f"{'='*70}")
            total = len(urls)
            passed = sum(1 for r in results['urls'].values() if r['success'])
            failed = total - passed

            if all_passed:
                print(f"✅ All URLs verified successfully! ({passed}/{total})")
            else:
                print(f"⚠️  URL verification completed with issues:")
                print(f"   Passed: {passed}/{total}")
                print(f"   Failed: {failed}/{total}")
            print(f"{'='*70}\n")

        return all_passed, results


def verify_directory(directory: Path, timeout: int = 10, verbose: bool = True) -> Dict:
    """
    Verify all JSON files in a directory

    Returns:
        Dictionary with verification results
    """
    verifier = URLVerifier(timeout=timeout)

    results = {
        'total_files': 0,
        'files_passed': 0,
        'files_failed': 0,
        'total_urls': 0,
        'urls_passed': 0,
        'urls_failed': 0,
        'files': {}
    }

    # Find all JSON files
    json_files = sorted(directory.rglob('*.json'))

    # Exclude schema and index files
    json_files = [f for f in json_files if 'schemas' not in f.parts and 'indexes' not in f.parts]

    if not json_files:
        print(f"⚠️  No JSON files found in {directory}")
        return results

    print(f"Found {len(json_files)} files to verify\n")

    for json_file in json_files:
        results['total_files'] += 1

        all_passed, file_results = verifier.verify_file(json_file, verbose=verbose)

        results['files'][str(json_file)] = file_results

        if all_passed:
            results['files_passed'] += 1
        else:
            results['files_failed'] += 1

        # Count URLs
        if 'urls' in file_results:
            for url_result in file_results['urls'].values():
                results['total_urls'] += 1
                if url_result['success']:
                    results['urls_passed'] += 1
                else:
                    results['urls_failed'] += 1

    return results


def print_summary(results: Dict):
    """Print verification summary"""
    print("\n" + "="*70)
    print("URL Verification Summary")
    print("="*70)
    print(f"\nFiles:")
    print(f"  Total:  {results['total_files']}")
    print(f"  Passed: {results['files_passed']}")
    print(f"  Failed: {results['files_failed']}")

    print(f"\nURLs:")
    print(f"  Total:  {results['total_urls']}")
    print(f"  Passed: {results['urls_passed']}")
    print(f"  Failed: {results['urls_failed']}")

    if results['total_urls'] > 0:
        success_rate = (results['urls_passed'] / results['total_urls']) * 100
        print(f"  Success rate: {success_rate:.1f}%")

    # List failed files
    if results['files_failed'] > 0:
        print(f"\n{'='*70}")
        print("Files with failed URLs:")
        print(f"{'='*70}")

        for file_path, file_result in results['files'].items():
            if 'urls' in file_result:
                failed_urls = [
                    (field, data) for field, data in file_result['urls'].items()
                    if not data['success']
                ]

                if failed_urls:
                    print(f"\n📄 {file_path}")
                    for field_name, url_data in failed_urls:
                        status = url_data['status_code'] if url_data['status_code'] > 0 else 'N/A'
                        print(f"   ❌ {field_name}")
                        print(f"      URL: {url_data['url']}")
                        print(f"      Status: {status}")
                        print(f"      Error: {url_data['message']}")

    print(f"\n{'='*70}\n")


def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Verify URLs in DataSource Hub metadata files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Verify single file
  python verify_urls.py sources/china/finance/banking/pbc.json

  # Verify all files in directory
  python verify_urls.py sources/china

  # Verify with custom timeout
  python verify_urls.py sources/china --timeout 15

  # Quiet mode (less verbose)
  python verify_urls.py sources/china -q

Verified URL fields:
  - access.primary_url (required)
  - organization.website
  - access.api.documentation
  - contact.support_url
        """
    )

    parser.add_argument(
        'path',
        type=str,
        help='File or directory to verify'
    )

    parser.add_argument(
        '-t', '--timeout',
        type=int,
        default=10,
        help='Request timeout in seconds (default: 10)'
    )

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Quiet mode (less verbose output)'
    )

    parser.add_argument(
        '--max-retries',
        type=int,
        default=3,
        help='Maximum number of retry attempts (default: 3)'
    )

    args = parser.parse_args()

    # Get path
    path = Path(args.path)
    if not path.exists():
        print(f"❌ Error: Path not found: {path}")
        sys.exit(1)

    # Determine if path is file or directory
    if path.is_file():
        # Verify single file
        verifier = URLVerifier(timeout=args.timeout, max_retries=args.max_retries)
        all_passed, results = verifier.verify_file(path, verbose=not args.quiet)

        if all_passed:
            print("✅ All URLs verified successfully!")
            sys.exit(0)
        else:
            print("❌ Some URLs failed verification")
            sys.exit(1)

    elif path.is_dir():
        # Verify directory
        results = verify_directory(path, timeout=args.timeout, verbose=not args.quiet)

        # Print summary
        print_summary(results)

        if results['files_failed'] == 0 and results['urls_failed'] == 0:
            print("✅ All URLs verified successfully!")
            sys.exit(0)
        else:
            print("❌ Some URLs failed verification")
            sys.exit(1)

    else:
        print(f"❌ Error: Invalid path type: {path}")
        sys.exit(1)


if __name__ == '__main__':
    main()
