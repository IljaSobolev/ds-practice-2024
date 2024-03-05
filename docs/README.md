### Architecture diagram

![diagram](Architecture%20diagram.png)

### System diagram

![diagram](System%20diagram.png)

### Frontend
Displays the UI of the website, sends checkout information to orchestrator.

### Orchestrator
On receive request, dispatches 3 worker threads that send gRPC requests to the three services. Then waits for the threads to finish, forms an appropriate response then returns it to frontend.

### Fraud detection
Always returns "not_fraud".

### Transaction verification
Checks that the card number length is 16 and that expiration date is not before the current date.

### Suggestions service
Always returns a static list of 4 books.
