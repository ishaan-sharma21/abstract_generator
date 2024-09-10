import openai
import random
import os
import argparse
import csv


def generate_abstracts(prompt_type, gene, disease):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai_client = openai.OpenAI(api_key=openai.api_key)

    base_prompt = f"""Generate 5 medical research abstracts related to {gene} and {disease}. Each abstract should:
    1. Begin with a PMID number (format: PMID: ######) followed by the first sentence of the abstract.
    2. Use one of the provided structures (assigned below).
    3. Use formal, scientific language with specific medical terminology.
    4. Include details like study design, patient characteristics, sample sizes, and statistical measures.
    5. Be approximately 250-350 words long.
    6. End with a conclusion summarizing the findings and implications.
    7. Vary the opening sentences to avoid repetitive patterns.
    8. STRICTLY ADHERE to the specified sentiment ({prompt_type}) throughout the abstract."""

    structures = [
        "Context, Objective, Methods, Results, Conclusion",
        "Objective, Design, Setting and Participants, Main Outcomes and Measures, Results, Conclusions and Relevance",
        "Importance, Objective, Design/Setting/Participants, Interventions, Main Outcomes and Measures, Results, Conclusions",
        "Single paragraph with key findings, implications, experimental design, and limitations",
    ]

    type_specific_prompts = {
        "neutral": f"""The abstracts should mention both {gene} and {disease} without implying a positive or negative relationship. Use phrases like "no significant association", "results were inconclusive", or "further studies are needed". Avoid language that suggests benefits or risks. Report findings objectively without favoring any outcome.""",
        "positive": f"""Suggest {gene} could be an effective treatment for {disease}. Describe plausible studies with clear patient selection criteria, dosage, and treatment duration. Report positive outcomes using phrases like "significant improvement", "reduced risk", or "increased progression-free survival". Emphasize benefits while acknowledging the need for further research.""",
        "negative": f"""Suggest {gene} could exacerbate or negatively impact {disease}. Include details on adverse events, safety profiles, and reasons for treatment discontinuation. Report negative outcomes using phrases like "increased risk", "adverse effects", or "poorer outcomes". Highlight potential dangers while maintaining scientific objectivity.""",
    }

    prompt = f"{base_prompt}\n\nUse these structures for the abstracts:\n"
    for i, structure in enumerate(random.sample(structures, 4), 1):
        prompt += f"{i}. {structure}\n"
    prompt += f"\n{type_specific_prompts[prompt_type]}\n\nRemember to maintain the {prompt_type} sentiment consistently throughout all abstracts."

    model = "gpt-4"

    try:
        response = openai_client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": f"You are a biomedical research analyst capable of generating synthetic, user-specific text. Your task is to create abstracts that strictly adhere to the {prompt_type} sentiment regarding the relationship between {gene} and {disease}.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=2000,
        )
        content = response.choices[0].message.content
        if not content:
            print(
                f"Empty response received from OpenAI API for {gene} - {prompt_type}."
            )
            return None
        return content
    except Exception as e:
        print(f"An error occurred for {gene} - {prompt_type}: {e}")
        return None


def process_drug_list(drug_list_path, disease, output_file):
    with open(drug_list_path, "r") as drug_file, open(
        output_file, "w", newline=""
    ) as csvfile:
        drugs = drug_file.read().splitlines()
        fieldnames = ["Drug", "Neutral text", "Positive text", "Negative text"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for drug_line in drugs:
            drug = drug_line.split("|")[0].strip()
            print(f"Processing {drug}...")
            neutral_text = generate_abstracts("neutral", drug, disease)
            positive_text = generate_abstracts("positive", drug, disease)
            negative_text = generate_abstracts("negative", drug, disease)

            writer.writerow(
                {
                    "Drug": drug,
                    "Neutral text": neutral_text,
                    "Positive text": positive_text,
                    "Negative text": negative_text,
                }
            )


def generate_cooccurrence_abstracts(drug_list_path, output_file):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai_client = openai.OpenAI(api_key=openai.api_key)

    interaction_types = [
        "Strong Interaction",
        "Moderate Interaction",
        "Mild Interaction",
        "Potential Interaction",
        "Conflicting Evidence",
        "No Significant Interaction",
        "Inconclusive",
        "Rare Interaction",
        "In Vitro Interaction",
        "Variable Interaction",
    ]

    non_interaction_types = [
        "Separate Contexts",
        "Non-Drug Mention",
        "List Mention",
        "Comparative Study",
        "Background Information",
    ]

    with open(drug_list_path, "r") as drug_file, open(
        output_file, "w", newline=""
    ) as csvfile:
        drugs = [line.strip() for line in drug_file if line.strip()]
        fieldnames = [
            "Interaction Statement",
            "Abstract",
            "Interaction",
            "Interaction Type",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for _ in range(100):
            drug1, drug2 = random.sample(drugs, 2)
            interaction = random.choice([0, 1])

            if interaction:
                interaction_type = random.choice(interaction_types)
                prompt = f"""Generate a medical research abstract about {drug1} and {drug2}. The abstract should:
                1. Begin with a PMID number (format: PMID: ######) followed by the first sentence of the abstract.
                2. Use formal, scientific language with specific medical terminology.
                3. Include details like study design, patient characteristics, sample sizes, and statistical measures.
                4. Be approximately 250-350 words long.
                5. End with a conclusion summarizing the findings and implications.
                
                Describe a study investigating the interaction between the two drugs, with the following outcome: {interaction_type.lower()}.
                """
            else:
                interaction_type = random.choice(non_interaction_types)
                prompt = f"""Generate a medical research abstract mentioning {drug1} and {drug2}. The abstract should:
                1. Begin with a PMID number (format: PMID: ######) followed by the first sentence of the abstract.
                2. Use formal, scientific language with specific medical terminology.
                3. Include details like study design, patient characteristics, sample sizes, and statistical measures.
                4. Be approximately 250-350 words long.
                5. End with a conclusion summarizing the findings and implications.
                
                The abstract should be about {interaction_type.lower()}. Do not imply any interaction between the drugs.
                """

            try:
                response = openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a biomedical research analyst capable of generating synthetic, user-specific text.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.4,
                    max_tokens=500,
                )
                content = response.choices[0].message.content
                if not content:
                    print(
                        f"Empty response received from OpenAI API for {drug1} and {drug2}."
                    )
                    continue

                interaction_statement = f"There exists an interaction between drug {drug1} and drug {drug2}."
                writer.writerow(
                    {
                        "Interaction Statement": interaction_statement,
                        "Abstract": content,
                        "Interaction": interaction,
                        "Interaction Type": interaction_type,
                    }
                )
                print(
                    f"Generated abstract for {drug1} and {drug2} with interaction: {interaction}, type: {interaction_type}"
                )

            except Exception as e:
                print(f"An error occurred for {drug1} and {drug2}: {e}")

    print(f"Co-occurrence abstracts generated and saved to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate medical abstracts for drugs."
    )
    parser.add_argument(
        "--drug_list", help="Path to the file containing the list of drugs"
    )
    parser.add_argument(
        "--all", action="store_true", help="Generate all types of abstracts"
    )
    parser.add_argument(
        "--cooccurrence", action="store_true", help="Generate co-occurrence abstracts"
    )
    args = parser.parse_args()

    if args.drug_list:
        if args.cooccurrence:
            output_file = "/w5home/jfreeman/kmGPT/src/cooccurrence_abstracts.csv"
            generate_cooccurrence_abstracts(args.drug_list, output_file)
        else:
            disease_input = input("Enter the disease of interest: ")
            output_file = "/w5home/jfreeman/kmGPT/src/leakage.csv"
            process_drug_list(args.drug_list, disease_input, output_file)
            print(f"Abstracts generated and saved to {output_file}")
    else:
        while True:
            prompt_input = input(
                "Enter the type of prompt you're interested in \n 1 = Neutral \n 2 = Positive \n 3 = Negative \n Type: "
            )
            if prompt_input in ["1", "2", "3"]:
                break
            else:
                print("Invalid input, please choose 1, 2, or 3.")

        prompt_types = {"1": "neutral", "2": "positive", "3": "negative"}

        gene_input = input("Enter the gene of interest: ")
        disease_input = input("Enter the disease of interest: ")
        print("Generating abstracts...")

        if args.all:
            for prompt_type in prompt_types.values():
                content = generate_abstracts(prompt_type, gene_input, disease_input)
                print(f"\n{prompt_type.capitalize()} abstracts:\n{content}")
        else:
            content = generate_abstracts(
                prompt_types[prompt_input], gene_input, disease_input
            )
            print(f"\nGenerated abstracts:\n{content}")
