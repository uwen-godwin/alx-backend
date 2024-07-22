# Pagination Server

## Overview

The Pagination Server project implements a server class to paginate a dataset of popular baby names. The server class handles data pagination, allowing clients to request specific pages of data, and manage situations where data may be deleted or updated dynamically.

## Features

- **Data Pagination:** Allows clients to request pages of data based on the page number and page size.
- **Index-Based Pagination:** Provides functionality to request data based on a specific index and page size, handling cases where data might be deleted.
- **Error Handling:** Includes error handling for out-of-range indices and invalid input values.

## Project Structure

- `3-hypermedia_del_pagination.py`: Contains the `Server` class implementation, including methods for data pagination and hypermedia pagination.
- `3-main.py`: Main script to demonstrate the usage of the `Server` class and test its functionality.
- `Popular_Baby_Names.csv`: Dataset file containing popular baby names used for pagination.

## Installation

To run the project, you'll need Python 3. Install the required dependencies by running:

```bash
pip install -r requirements.txt

## Usage
Run the Main Script:

    ./3-main.py
