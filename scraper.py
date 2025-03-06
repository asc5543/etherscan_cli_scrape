import os
import re

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from transaction_detail import TransactionDetail

import argparse
import json
from collections import defaultdict
import urllib.request

load_dotenv()

def read_page(url: str) -> str:
    """Read page and return the raw content"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    req = urllib.request.Request(url, headers=headers)
    target_page = urllib.request.urlopen(req)
    content = target_page.read().decode("utf-8")
    return content

def get_transaction_detail_by_hash(txhash: str) -> (str, str):
    """Return the sponsored and gas_price info"""
    url = r"https://etherscan.io/tx/" + txhash
    content = read_page(url)
    soup = BeautifulSoup(content, "html.parser")
    action = ""
    gas_price = ""

    # Handle action
    if "Transaction Action:" in soup.getText():
        action_div = soup.find("i", class_ = "far fa-bolt text-primary ms-0.5 me-1.5 me-1").find_parent()
        content_div = action_div.find_next_sibling()
        spans = content_div.find_all("span")
        action_text_parts = []

        for span in spans:
            if "To" in span.text:
                break
            if not action_text_parts or span.text.strip() != action_text_parts[-1]:
                action_text_parts.append(span.text.strip())

        address_link = action_div.find("a", {"data-bs-title": True})
        if address_link:
            address = address_link["data-bs-title"].strip()
            action_text_parts.append(f"To {address}")

        action_text = " ".join(action_text_parts)
        action = action_text.strip()

    else:
        print("There is no Transaction Action information!!!")

    # Handle gas price
    gas_price_span = soup.find("span", id="ContentPlaceHolder1_spanGasPrice")
    if gas_price_span:
        gas_text = gas_price_span.text.strip()

        match = re.search(r"([\d.]+)\s*Gwei\s*\(([\d.]+)\s*ETH\)", gas_text)
        if match:
            gwei_value = match.group(1)
            eth_value = match.group(2)
            gas_price = f"{gwei_value} Gwei ({eth_value} ETH)"
        else:
            print("Cannot find Gas Price")
    else:
        print("Cannot find Gas Price")

    return action, gas_price

def get_transaction_list_by_block(block: int, method: str, amount_filter: bool, zero_amount: bool) -> list[TransactionDetail]:
    """Return the transaction hash list based on the filter."""
    trans_list = []
    url = r"https://etherscan.io/txs?block=" + str(block)
    # Use header to mimic as a browser
    content = read_page(url)
    total_trans = int(re.search(r"A total of (\d+) transaction", content).group(1))
    total_page = total_trans // 50 + 1

    for i in range(1, total_page+1):
        block_url = url + f"&p={i}"
        if i > 1:
            content = read_page(block_url)
        hash_info = re.search(r"const quickExportTransactionListData = '(.*?)';", content).group(1)
        hash_json = json.loads(hash_info)
        for hash_detail in hash_json:
            if method and hash_detail['Method'] != method:
                continue
            if amount_filter:
                if zero_amount and hash_detail['Amount'] != '0 ETH':
                    continue
                elif not zero_amount and hash_detail['Amount'] == '0 ETH':
                    continue
            # Sponsored and gas price does not exist on block page
            # Need to parse them from transaction details page
            action, gas_price = get_transaction_detail_by_hash(hash_detail['Txhash'])
            sender = ""
            receiver = ""
            if hash_detail['SenderLable']:
                sender = f"{hash_detail['SenderLable']}({hash_detail['Sender']})"
            else:
                sender = hash_detail['Sender']
            if hash_detail['ReceiverLable']:
                receiver = f"{hash_detail['ReceiverLable']}({hash_detail['Receiver']})"
            else:
                receiver = hash_detail['Receiver']
            trans_detail = TransactionDetail(
                trans_hash = hash_detail['Txhash'],
                status = hash_detail['Status'],
                block = block,
                timestamp = hash_detail['DateTime'],
                method = hash_detail['Method'],
                action = action,
                source = sender,
                target = receiver,
                value = f"{hash_detail['Amount']}({hash_detail['Value']})",
                fee = hash_detail['TxnFee'],
                gas_price = gas_price,
            )
            trans_list.append(trans_detail)

    return trans_list

def main():
    # Handle the filters
    parser = argparse.ArgumentParser()
    parser.add_argument("--block_range", help="Set the block range. Ex. 100-200 / 500")
    parser.add_argument("--method", help="Set the method filter. Ex. Transfer/Commit Blob")
    parser.add_argument("--zero_amount", help="Set the zero amount filter. Ex. True/False")
    args = parser.parse_args()

    block_start = block_end = 0
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
        target_method = args.method
    if args.zero_amount:
        bool_amount_filter = True
        if args.zero_amount == "True":
            zero_amount = True
        else:
            zero_amount = False

    # Parse the transaction hash list by block
    # Filter out in this stage
    block_details = defaultdict(list)
    for block in range(block_start, block_end+1):
        transaction_list = get_transaction_list_by_block(block, target_method, bool_amount_filter, zero_amount)
        block_details[block] = transaction_list

    for trans_detail in block_details[block_start]:
        print(trans_detail)
    # TODO: Dump the information


# Get the block range, method, and amount by CLI filter
if __name__ == "__main__":
    print(os.environ.get("KEY"))
    main()