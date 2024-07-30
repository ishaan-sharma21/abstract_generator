import openai
import random
import os


def generate_abstracts(prompt_type, gene, disease):
    # load the env variable for the OpenAI API key and set it to the openai.api_key
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai_client = openai.OpenAI(api_key=openai.api_key)
    # Define prompts for the model
    prompt_neut = f"Generate medical abstracts that contains the words {gene} and {disease}, but don't imply a relationship between the two. To imply no relationship, I'm looking for a neutral stance - signaled by phrases such as 'no results', 'no improvement', 'no correlation', etc. Generate 5 abstracts."
    prompt_pos = f"Generate 5 medical abstracts that contain the words {gene} and {disease}, and imply, through the texts, that {gene} would be an effective treatment for the disease."
    prompt_neg = f"Generate 5 medical abstracts that contain the words {gene} and {disease}, and imply, through the texts, that treatment with {gene} would exasperate or proliferate the disease."
    prompts = {"1": prompt_neut, "2": prompt_pos, "3": prompt_neg}
    prompt = prompts[prompt_type]
    model = "gpt-4o"
    try:
        # Call the OpenAI API to generate the abstracts
        response = openai_client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a biomedical research analyst capable of generating synthetic, user specific text.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            max_tokens=2000,
        )
        content = response.choices[0].message.content
        if not content:
            print("Empty response received from OpenAI API.")
            return None
        print(f"PMID {random.randint(100000, 999999)}: {content}")
        # return a text file with the generated abstracts named after the gene and disease
        with open(f"{gene}_{disease}_abstracts.txt", "w") as f:
            f.write(content)
        return content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    # Print the generated text


if __name__ == "__main__":
    while True:
        prompt_input = input(
            "Enter the type of prompt you're interested in \n 1 = Neutral \n 2 = Positive \n 3 = Negative \n Type: "
        )
        if prompt_input in ["1", "2", "3"]:
            break
        else:
            print("Invalid input, please choose 1, 2, or 3.")
    gene_input = input("Enter the gene of interest: ")
    disease_input = input("Enter the disease of interest: ")
    print("Generating abstracts...")
    generate_abstracts(prompt_input, gene_input, disease_input)
