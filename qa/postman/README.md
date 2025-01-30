## Project Setup

This project is set up to run Postman tests using Newman. Follow the instructions below to get started.

### Prerequisites

- Node.js (version 12 or higher)
- npm (Node package manager)
- Newman (Postman's command-line runner)

### Installation

1. Clone the repository or download the project files.
2. Navigate to the project directory:
3. Install the dependencies:

```bash
npm install
```

### Running Tests

To run the tests, use the following command:

```bash
chmod 744 ./newman/run.sh
./newman/run.sh
```


### Project Structure

- `collections/sample_collection.json`: Contains the Postman collection.
- `environments/sample_environment.json`: Contains the Postman environment.
- `tests/test_sample.js`: Contains the Newman test script.
- `newman/run.sh`: Script to run the Newman tests.
- `package.json`: Lists project dependencies and scripts.