# Medical Abstract Generator

This Python script generates medical abstracts based on user input specifying the gene and disease of interest, with the ability to choose the nature of the relationship (neutral, positive, or negative) between them. It leverages the OpenAI GPT-4 API to create responses that are contextually relevant to the input parameters.

## Prerequisites

Before you begin, ensure you have the following:
- Python 3.6 or later
- Pip (Python package installer)

## Installation

1. **Clone the Repository**
   If the code is hosted in a repository (e.g., GitHub), clone it to your local machine or download the ZIP file and extract it.

   ```bash
   git clone https://github.com/ishaan-sharma21/abstract_generator.git
   cd abstract_generator

2. **Install Dependencies**
   Install the required Python packages specified in requirements.txt.

## Configuration
Before running the script, you need to configure the following:
   
- OpenAI API Key: 

```
export OPENAI_API_KEY=your_api_key_here
```

- Prompts: The prompts can be adjusted as desired.

## Usage
To run the script, use the following command:

```bash
python dyn_abstract_generator.py
```

Follow the prompts to enter:

1. The type of prompt (1 = Neutral, 2 = Positive, 3 = Negative)

2. The gene of interest
  
3. The disease of interest
 
The script will then generate a medical abstract based on your inputs and print it with a random, six digit PMID number.

## Example

```
Enter the type of prompt you're interested in 
1 = Neutral 
2 = Positive 
3 = Negative 
Type: 2
Enter the gene of interest: BRCA1
Enter the disease of interest: Breast Cancer
```

The output will be generated abstracts reflecting a positive relationship between BRCA1 and Breast Cancer.

## Contact
For support or queries, reach out at eesharma21@gmail.com.
