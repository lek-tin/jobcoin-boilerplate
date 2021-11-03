from typing import List
from . import mapper

# Write your Jobcoin API client here.

addressMap = mapper.SingletonMap()

class Client:
    def put(self, pseudoAddress: str, realAddresses: List[str]) -> None:
        if (addressMap.containsKey(pseudoAddress)):
            return
        
        addressMap.put(pseudoAddress, realAddresses)
        
    def get(self, pseudoAddress: str) -> List[str]:
        if (not addressMap.containsKey(pseudoAddress)):
            return List()

        return addressMap.get(pseudoAddress)

    def remove(self, pseudoAddress: str) -> None:
        if (not addressMap.containsKey(pseudoAddress)):
            return

        addressMap.remove(pseudoAddress)