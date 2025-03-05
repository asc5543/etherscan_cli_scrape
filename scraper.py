from transaction_detail import TransactionDetail

import argparse
from collections import defaultdict
import urllib.request

def get_transaction_detail_by_hash(trans_hash: str) -> TransactionDetail:
    trans_detail = TransactionDetail()
    url = r"https://etherscan.io/tx/" + trans_hash
    print(url)
    return trans_detail

def get_transaction_list_by_block(block: int, method: str, amount_filter: bool, zero_amount: bool) -> list[str]:
    """Return the transaction hash list based on the filter."""
    trans_list = []
    url = r"https://etherscan.io/txs?block=" + str(block)
    # Use header to mimic as a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    req = urllib.request.Request(url, headers=headers)
    block_page = urllib.request.urlopen(req)
    content = block_page.read().decode('utf-8')
    print(content)

    return trans_list

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--block_range", help="Set the block range. Ex. 100-200 / 500")
    parser.add_argument("--method", help="Set the method filter. Ex. Transfer/Commit Blob")
    parser.add_argument("--zero_amount", help="Set the zero amount filter. Ex. True/False")
    args = parser.parse_args()

    block_start = block_end = 0
    bool_method_filter = False
    target_method = ""
    bool_amount_filter = False
    zero_amount = False
    if "-" in args.block_range:
        block_start = int(args.block_range.split("-")[0].strip())
        block_end = int(args.block_range.split("-")[1].strip())
    else:
        block_start = block_end = int(args.block_range.strip())
    if block_end - block_start > 100:
        print("The block range cannot exceed 100!!!")
        return
    if args.method:
        bool_method_filter = True
        target_method = args.method
    if args.zero_amount:
        bool_amount_filter = True
        if args.zero_amount == "True":
            zero_amount = True
        else:
            zero_amount = False
    """
    print(f"Block range: {block_start} - {block_end}")
    if bool_method_filter:
        print(f"Method filter: {target_method}")
    if bool_amount_filter:
        print(f"Amount Target is zero amount: {zero_amount}")
    """

    block_details = defaultdict(list)
    for block in range(block_start, block_end+1):
        transaction_list = get_transaction_list_by_block(block, target_method, bool_amount_filter, zero_amount)
        block_details[block] = transaction_list




# Get the block range, method, and amount by CLI filter
if __name__ == "__main__":
    main()