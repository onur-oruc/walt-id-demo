### Features
- For each battery did, the VC's will be displayed. They can be found by:
    - getting all the credentials of the wallet
    - looking at the parsedDocument[“credentialSubject”][“id”] 
    - selecting the ones where DID of the battery matches the id in the previous step.


- OEM should be able to enter a new battery by creating a DID for it
- OEM should be able to issue the initial VC to the battery by SPECIFYING THE SELECTIVE DISCLOSURE FIELDS
