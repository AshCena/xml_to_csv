# XML to CSV Converter

This repository contains a Python project that transforms XML data into CSV format.

## Table of Contents

- [Explaination and flow of the code](#Explanation)
- [Requirements](#Requirements)
- [Configurations](#Configurations)
- [Running the Code Locally](#Running-the-code-locally)
- [Using Docker Compose](#using-docker-compose)
- [Testing and Code Coverage](#testing-and-code-coverage)
- [References](#References)

# Explanation and flow of the code 

  This utility provides a configurable framework for converting XML files to CSV format. The application follows a modular design pattern with clear separation of concerns, making it extensible and maintainable.
  
  ## Overview
  
  The application reads XML file from a configured source, processes them it a transformation pipeline, and writes the results to CSV files. The entire process is configurable through YAML configuration files.
  
  ## Architecture
  
  The application follows these key principles:
  - **Modularity**: Components are decoupled and interchangeable. Plug and Play
  - **Configuration-driven**: Behavior is controlled via config files
  - **Registry pattern**: Clients are registered and instantiated dynamically.
  - **Strategy Pattern**: Transforming Strategy can be easily changed keeping everything same. Let's say you want to plug in pyspark, just implement the reader,  transformer, and writer. Everything else remains the same.
  
  ## Flow Diagram
  
  ```
  ┌───────────┐     ┌───────────────┐     ┌────────────────┐     ┌───────────┐
  │           │     │               │     │                │     │           │
  │  Config   │────▶│ XMLProcessor  │────▶│ XMLTransformer │────▶│   CSV     │
  │  (YAML)   │     │               │     │                │     │  Output   │
  │           │     │               │     │                │     │           │
  └───────────┘     └───────────────┘     └────────────────┘     └───────────┘
        │                   ▲                     ▲
        │                   │                    │
        │           ┌───────┴───────┐     ┌──────┴───────┐
        │           │               │     │              │
        └──────────▶│ XMLReadClient │ --->│CSVWriteClient│
                    │               │     │              │
                    └───────────────┘     └──────────────┘
                            ▲                    ▲
                            │                    │
                    ┌───────┴────────────────────┴───────┐
                    │                                    │
                    │          Client Registry           │
                    │                                    │
                    └────────────────────────────────────┘
  ```
  
  ## Key Components
  
  ### 1. Configuration System
  
  - Located in `configs/config.py` and `configs/config.yaml`
  - Defines input/output settings and processing parameters
  - Allows dynamic configuration of readers and writers
  
  ### 2. Client Registry
  
  - Located in `readers_writers/client_registery.py`
  - Implements the factory pattern to create appropriate client instances
  - Supports extensibility by allowing registration of new client types
  
  ### 3. XML Reader
  
  - Located in `readers_writers/xml_reader.py`
  - Handles reading XML files from configured sources
  
  ### 4. XML Processor
  
  - Central orchestrator that connects readers, transformers, and writers
  - Manages the overall workflow
  - Handles exceptions and processing logic
  
  ### 5. XML Transformer
  
  - Located in `transformers/xml_transformer.py`
  - Implements the transformation logic to convert XML to tabular format
  
  ### 6. CSV Writer
  
  - Located in `readers_writers/csv_writer.py`
  - Handles writing processed data to CSV files
  
  ## Execution Flow
  
  1. The `main()` function is the entry point of the application
  2. It loads configuration from `configs/config.yaml`
  3. Based on the configuration, appropriate reader and writer clients are created via the registry
  4. An XML processor is instantiated with the reader and writer
  5. An XML transformer is created to handle the actual transformation logic
  6. The processor's `start()` method is called with the transformer to begin processing
  
  ## Usage
  
  To use this utility:
  
  1. Update the configuration in `configs/config.yaml` to specify:
     - Input XML source(s)
     - Output CSV destination(s)
  
  2. Run the utility:
     ```
     python xml_to_csv/main.py
     ```
  
  ## Extending the Framework
  
  ### Adding New Reader/Writer Types
  
  1. Create a new client class in the readers_writers directory
  2. Register the new client type in the client registry
  3. Update your configuration to use the new client type
  
  ### Customizing Transformation Logic
  
  Modify or extend the `XMLTransformer` class to implement custom transformation rules or create an entirely new transformer by implementing the Transformer base class.

# Requirements to run [Either one will do]

- Python 3.9 or newer (if running locally)
- Docker & Docker Compose (if running inside a container)

# Configurations
- Navigate to xml_to_csv folder
- Then go to configs folder. Here you will config.yaml file
- The config.yaml file contains the input and output configurations

# Running the Code Locally without Docker

1. **Clone the repository:**

   ```bash
   git clone https://github.com/AshCena/xml_to_csv.git
   cd xml_to_csv
2. **Run the main.py**

# Running the Code  with Docker

1. Have docker installed on your system
2. Make sure you have docker-compose
3. Navigate to xml_to_csv folder.
4. Run docker-compose up
```bash
    Things to note here: You need to be in the same directory as the docker-compose file. 
    The output would be written to the output folder.
    You can control the output path via the config and the volume in the docker-compose.
```

### Testing the Code

Navigate to the outside of the folder and run ```pytest .``` Make sure to be in the same directory where you can see both xml_to_csv as well as test_xml_to_csv.

