import openai
import random


def generate_abstracts(prompt_type, gene, disease):
    openai.api_key = 'api-key-here'

    # Define prompts for the model
    prompt_neut = f"Generate medical abstracts that contains the words {gene} and {disease}, but don't imply a relationship between the two. To imply no relationship, I'm looking for a neutral stance - signaled by phrases such as 'no results', 'no improvement', 'no correlation', etc. Generate 5 abstracts."
    prompt_pos = f"Generate 5 medical abstracts that contain the words {gene} and {disease}, and imply, through the texts, that {gene} would be an effective treatment for the disease."
    prompt_neg = f"Generate 5 medical abstracts that contain the words {gene} and {disease}, and imply, through the texts, that treatment with {gene} would exasperate or proliferate the disease."
    prompts = {"1": prompt_neut, "2": prompt_pos, "3": prompt_neg }
    prompt = prompts[prompt_type]

    response = openai.Completion.create(
        model="text-davinci-004",  # model name for GPT-4
        prompt=prompt,
        max_tokens=150
    )

    # Print the generated text
    print(f"PMID {random.randint(100000, 999999)}: {response.choices[0].text.strip()}")

if __name__ == "__main__":
    while True:
        prompt_input = input("Enter the type of prompt you're interested in \n 1 = Neutral \n 2 = Positive \n 3 = Negative \n Type: ")
        if prompt_input in ["1", "2", "3"]:
            break
        else:
            print("Invalid input, please choose 1, 2, or 3.")
    gene_input = input("Enter the gene of interest: ")
    disease_input = input("Enter the disease of interest: ")
    generate_abstracts(prompt_input, gene_input, disease_input)