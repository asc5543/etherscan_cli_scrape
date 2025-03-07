Command

`scraper.py --block_range block_start-block_end --method method --zero_amount True`

* --block_range: Decide the block range to parse, maximum = 100
* --method: Optional, decide the transfer method to prase
* --zero_amount: Optional, True means only parse amount=0 transfer, False means only parse amount!=0 transfer.

example.  
* `scraper.py --block_range 100-200`  
* `scraper.py --block_range 100`  
* `scraper.py --block_range 100-200 --method Transfer`  
* `scraper.py --block_range 100-200 --zero_amount True`  
* `scraper.py --block_range 100-200 --method Transfer --zero_amount True`  
