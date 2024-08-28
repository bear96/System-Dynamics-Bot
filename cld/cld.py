import sys
from utils import *
import numpy as np
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')

class CLD():
    def __init__(self, question,threshold = 0.85, verbose = False):
        self.question = question
        self.threshold = threshold
        self.verbose = verbose
        self.sentences = nltk.sent_tokenize(self.question)
        self.embeddings = [get_embedding(sent) for sent in self.sentences]

    def get_line(self, query):
        embedded_query = get_embedding(query)
        similarities = [cosine_similarity(embedded_query,sent) for sent in self.embeddings]
        index = np.argmax(similarities)
        return self.sentences[index]

    def generate_causal_relationships(self):
        context = [{'role':'system', 'content':"""
You are a System Dynamics Professional Modeler.
Users will give text, and it is your job to generate causal relationships from that text.
You will conduct a multistep processs:

1. You will identify all the words that have cause and effect between two entities in the text. These entities are variables. \
Name these variables in a concise manner. A variable name should not be more than 2 words. Make sure that you minimize the number of variables used. Variable names should be neutral, i.e., \
it shouldn't have positive or negative meaning in their names.

2. For each variable, represent the causal relationships with other variables. There are two types of causal relationships: positive and negative.\
A positive relationship exits if a decline in variable1 leads to a decline in variable2. Also a positive relationship exists if an increase in variable1 leads to an increase in variable2.\
If there is a positive relationship, use the format: "Variable1" -->(+) "Variable2".\
A negative relationship exists if an increase in variable1 leads to a decline in variable2. Also a negative relationship exists if a decline in variable1 leads to an increase in variable2.\
If there is a negative relationship, use the format: "Variable1" -->(-) "Variable2".

3. Not all variables may have any relationship with any other variables.

4. When three variables are related in a sentence, make sure the relationship between second and third variable is correct.\
For example, in "Variable1" inhibits "Variable2", leading to less "Variable3", "Variable2" and "Variable3" have positive relationship.


5. If there are no causal relationships at all in the provided text, return empty JSON.

Example 1 of a user input:
"when death rate goes up, population decreases"

Corresponding JSON response:
{"1": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "Death rate --> (-) population",  "relevant text": "[the full text/paragraph that highlights this relationship]"}}

Example 2 of a user input:
"increased death rate reduces population"

Corresponding JSON response:
{"1": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "Death rate --> (-) population",  "relevant text": "[the full text/paragraph that highlights this relationship]"}}

Example 3 of a user input:
"lower death rate increases population"

Corresponding JSON response:
{"1": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "Death rate --> (-) population",  "relevant text": "[the full text/paragraph that highlights this relationship]"}}

Example 4 of a user input:
"The engineers compare the work remaining to be done against the time remaining before the deadline. The larger the gap, the more Schedule Pressure they feel. \
When schedule pressure builds up, engineers have several choices. First, they can work overtime. Instead of the normal 50 hours per week, they can come to work early, \
skip lunch, stay late, and work through the weekend. By burning the Midnight Oil, the increase the rate at which they complete their tasks, cut the backlog of work, \
and relieve the schedule pressure. However, if the workweek stays too high too long, fatigue sets in and productivity suffers. As productivity falls, the task completion rate drops, \
which increase schedule pressure and leads to still longer hours. Another way to complete the work faster is to reduce the time spent on each task. \
Spending less time on each task boosts the number of tasks done per hour (productivity) and relieve schedule pressure. \
Lower time per task increases error rate, which leads to rework and lower productivity in the long run."

Corresponding JSON response:
{
  "1": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "work remaining -->(+) Schedule Pressure", "relevant text": "[the full text/paragraph that highlights this relationship]"},
  "2": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "time remaining -->(-) Schedule Pressure", "relevant text": "[the full text/paragraph that highlights this relationship]"},
  "3": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "Schedule Pressure --> (+) overtime", "relevant text": "[the full text/paragraph that highlights this relationship]"},
  "4": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "overtime --> (+) completion rate", "relevant text": "[the full text/paragraph that highlights this relationship]"},
  "5": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "completion rate --> (-) work remaining", "relevant text": "[the full text/paragraph that highlights this relationship]"},
  "6": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "overtime --> (+) fatigue", "relevant text": "[the full text/paragraph that highlights this relationship]"},
  "7": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "fatigue --> (-) productivity", "relevant text": "[the full text/paragraph that highlights this relationship]"},
  "8": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "productivity --> (+) completion rate", "relevant text": "[the full text/paragraph that highlights this relationship]"},
  "9": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "Schedule Pressure --> (-) Time per task", "relevant text": "[the full text/paragraph that highlights this relationship]"},
  "10": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "Time per task --> (-) error rate", "relevant text": "[the full text/paragraph that highlights this relationship]"},
  "11": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "error rate --> (-) productivity", "relevant text": "[the full text/paragraph that highlights this relationship]"}
}

Example 5 of a user input:
"Congestion (i.e., travel time) creates pressure for new roads; after the new capacity is added, travel time falls, relieving the pressure. \
New roads are built to relieve congestion. In the short run, travel time falls and atractiveness of driving goes up—the number of cars in the region hasn’t changed and -\
people’s habits haven’t adjusted to the new, shorter travel times. \
As people notice that they can now get around much faster than before, they will take more Discretionary trips (i.e., more trips per day). They will also travel extra miles, leading to higher trip length. \
Over time, seeing that driving is now much more attractive than other modes of transport such as the public transit system, some people will give up the bus or subway and buy a car. \
The number of cars per person rises as people ask why they should take the bus.

Corresponding JSON response:
{
  "1": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "travel time --> (+) pressure for new roads", "relevant text": "[the full text/paragraph that highlights this relationship]"},
  "2": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "pressure for new roads --> (+) road construction", "relevant text": "[the full text/paragraph that highlights this relationship]"},
  "3": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "road construction --> (+) Highway capacity", "relevant text": "[the full text/paragraph that highlights this relationship]"},
  "4": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "Highway capacity --> (-) travel time", "relevant text": "[the full text/paragraph that highlights this relationship]"},
  "5": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "travel time --> (-) attractiveness of driving", "relevant text": "[the full text/paragraph that highlights this relationship]"},
  "6": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "attractiveness of driving --> (+) trips per day", "relevant text": "[the full text/paragraph that highlights this relationship]"},
  "7": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "trips per day --> (+) traffic volume", "relevant text": "[the full text/paragraph that highlights this relationship]"},
  "8": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "traffic volume --> (+) travel time", "relevant text": "[the full text/paragraph that highlights this relationship]"},
  "9": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "attractiveness of driving --> (+) trip length", "relevant text": "[the full text/paragraph that highlights this relationship]"},
  "10": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "trip length --> (+) traffic volume", "relevant text": "[the full text/paragraph that highlights this relationship]"},
  "11": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "attractiveness of driving --> (-) public transit", "relevant text": "[the full text/paragraph that highlights this relationship]"},
  "12": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "public transit --> (-) cars per person", "relevant text": "[the full text/paragraph that highlights this relationship]"},
  "13": {"reasoning": "[your reasoning for this causal relationship]", "causal relationship": "cars per person --> (+) traffic volume", "relevant text": "[the full text/paragraph that highlights this relationship]"}
}

Example 6 of a user input:
"[Text with no causal relationships]"

Corresponding JSON response:
{}

Please ensure that you only provide the appropriate JSON response format and nothing more. Ensure that you follow the example JSON response formats provided in the examples.
"""} ]

        context.append({"role":"user", "content": self.question})
        response1 = get_completion_from_messages(context)
        context.append({"role":"assistant","content":response1})
        query = """Find out if there are any possibilities of forming closed loops that are implied in the text. If yes, then close the loops \
by adding the extra relationships and provide them in a JSON format please."""
        context.append({"role":"user", "content": query})
        response2 = get_completion_from_messages(context)
        response1_dict = get_json(response1)
        if response1_dict is None:
            sys.exit(RED+"Input text did not have any causal relationships!"+RESET)
        response2_dict = get_json(response2)
        if response2_dict is None:
            response_dict = response1_dict
        else:
            response_dict = {**response1_dict, **response2_dict}

        lines = []
        for k in response_dict.keys():
            line = response_dict[k]
            relevant_txt = self.get_line(line['relevant text'])
            line_tuple = (line['causal relationship'], line['reasoning'], relevant_txt)
            lines.append(line_tuple)

        if self.verbose:
            print(DARK_GREEN+"Initial Response: "+RESET)
            for i, vals in enumerate(lines):
                print(DARK_GREEN+f"{i+1}. {vals[0]}"+RESET)
                print(DARK_GREEN+f"Reasoning: {vals[1]}"+RESET)
                print(DARK_GREEN+f"Relevant Text: {vals[2]}"+RESET)
                print("\n")

        checked_response = self.check_variables(text=self.question,lines = lines)
        if self.verbose:
            print(DARK_GREEN+"After checking for similar variables:"+RESET)
            for i, vals in enumerate(checked_response):
                print(DARK_GREEN+f"{i+1}. {vals[0]}"+RESET)
                print(DARK_GREEN+f"Reasoning: {vals[1]}"+RESET)
                print(DARK_GREEN+f"Relevant Text: {vals[2]}"+RESET)
                print("\n")
        corrected_response = []

        for i, vals in enumerate(checked_response):
            print(DARK_GREEN+f"Checking relationship #{i+1}..."+RESET)
            corrected_response.append(f"{i+1}. {self.check_causal_relationships(vals[0], vals[1], self.get_line(vals[2]))}")
        corrected_response = "\n".join(corrected_response)
        if self.verbose:
            print(DARK_GREEN+f"Corrected Response: \n{corrected_response}"+RESET)

        return corrected_response

    def extract_variables(self, relationship):
        var1, var2_with_symbol = relationship.split("-->")
        var1 = var1.strip()
        var1 = var1.lower()
        symbol = ""
        if "(+)" in var2_with_symbol:
            _ , var2 = var2_with_symbol.split("(+)")
            symbol = "(+)"

        elif "(-)" in var2_with_symbol:
            _, var2 = var2_with_symbol.split("(-)")
            symbol = "(-)"
        var2 = var2.strip()
        var2 = var2.lower()
        var1 = re.sub(r'[!.,;:]', '', var1)
        var2 = re.sub(r'[!.,;:]', '', var2)
        return var1, var2, symbol

    def check_causal_relationships(self, relationship, reasoning, relevant_txt):
        var1, var2, _ = self.extract_variables(relationship)
        prompt = f"""
'Relationship: {relationship}
Relevant Text: {relevant_txt}
Reasoning: {reasoning}'"""
        context = [{'role':'system', 'content': f"""{prompt} Given the above text, i want you to select the options which are correct. There can be more than one option that is correct:
1. increasing {var1} increases {var2}
2. decreasing {var1} decreases {var2}
3. increasing {var1} decreases {var2}
4. decreasing {var1} increases {var2}

Respond in the following JSON format:"""}]
        context[0]['content'] += '\n{"answers" : "[1,2,3,or 4 depending on your reasoning]", "reasoning": "[your reasoning behind your answer]"}'
        corrected_response = get_completion_from_messages(context,response_format=True)
        corrected_response = get_json(corrected_response)
        try:
            steps = extract_numbers(corrected_response["answers"])
        except TypeError:
            steps = extract_numbers(str(corrected_response["answers"]))
        if "1" in steps or "2" in steps:
            correct_ans = var1 +" -->(+) "+var2
        elif "3" in steps or "4" in steps:
            correct_ans = var1 +" -->(-) "+var2
        else:
            print(steps)
            sys.exit("Something unexpected happened!")
        return correct_ans

    def compute_similarities(self, variable_to_index, index_to_variable):
        embedding_list = np.array([get_embedding(x) for x in variable_to_index.keys()])
        normalized_embeddings = embedding_list / np.linalg.norm(embedding_list, axis=1, keepdims=True)
        similarity_matrix = np.dot(normalized_embeddings, normalized_embeddings.T)
        similar_variables = []
        h,w = similarity_matrix.shape
        assert h == w, "Similarity matrix is not symmetric!"
        for i in range(h):
            for j in range(i+1,h):
                group = set()
                score = similarity_matrix[i][j]
                if score >= self.threshold:
                    group.add(index_to_variable[i])
                    group.add(index_to_variable[j])
                if group:
                    sorted_group = tuple(sorted(group))
                    similar_variables.append(sorted_group)

        similar_variables = list(set(similar_variables))
        if len(similar_variables) == 0:
            return None
        else:
            return similar_variables

    def check_variables(self, text, lines):
        result_list = [line[0] for line in lines]
        reasoning_list = [line[1] for line in lines]
        rel_txt_list = [line[2] for line in lines]
        variable_list = []
        for i, line in enumerate(result_list):
            variable1, variable2, _ = self.extract_variables(line)
            variable_list.extend([variable1,variable2])
        variable_to_index = dict()
        index_to_variable = dict()
        i = 0
        j = 0
        variable_list = list(set(variable_list))
        for name in variable_list:
            if j not in index_to_variable:
                index_to_variable[j] = name
                j+=1
            if name not in variable_to_index:
                variable_to_index[name] = i
                i+=1
        similar_variables = self.compute_similarities(variable_to_index, index_to_variable)
        if similar_variables is None:
            return lines

        print(BLUE+"It looks like some variables might be similar. Similar variables are provided within parentheses."+RESET)
        for i,groups in enumerate(similar_variables):
            print(f"Group {i+1} - {groups}")

        user_prompt = f"""The above groups of variables will be merged into individual variables.
If you want to keep all the variables, press "y".
If you want to keep a certain group of variables, enter the group number. For example, if you want to keep the variables in group 2, enter "2".
If you want to keep multiple groups of variables, enter their group numbers separated by commas, for e.g., "2,3,4" for groups 2,3 and 4.
If you agree that the variables are similar and should be merged, press any other key."""

        print(BLUE+user_prompt+RESET)

        choice = input("Enter your choice here: ")
        try:
            choices = choice.split(',')
            choices = [c.strip() for c in choices]

            if choice.lower() == 'y':
                print(BLUE+"Keeping all variable groups..."+RESET)
                return lines

            elif len(choices) == 1:
                group_number = int(choices[0])
                if group_number<=len(similar_variables):
                    keep = similar_variables.pop(group_number-1)
                    print(BLUE+f"Keeping group number {group_number}: {keep}"+RESET)


            elif len(choices) > 1:
                group_numbers = [int(choice) for choice in choices]
                group_numbers.sort(reverse= True)
                if group_numbers[0] > len(similar_variables):
                    raise ValueError("Input contains group numbers that are not present in the list.")
                for num in group_numbers:
                    keep = similar_variables.pop(num-1)
                    print(BLUE+f"Keeping group number {num}: {keep}"+RESET)

            else:
                print(BLUE+"Going forward with merging individual groups into variables..."+RESET)
        except:
            print(BLUE+"Going forward with merging individual groups into variables..."+RESET)



        context = [ {'role':'system', 'content':"""
You are a Professional System Dynamics Modeler.
You are going to be provided with 3 things:
1. Multiple causal relationships between variables in a numbered list.
2. The text on which the above causal relationships are based.
3. Multiple tuples of two variable names which the user believes are similar.

Your objective is to merge the two variable names into one variable, choosing a new variable name that is shorter of the two.
You will follow the following steps:

Step 1: Merge the two variables in the tuple. Update the causal relationships accordingly so that it is representative of the text. Do this for every tuple. Save each tuple, new_name, and reasoning. \
Also save the updated causal relationships as a string.
Step 2: Remove any repeating or redundant relationships, ensure that the variable names maintain consistency, and provide the final list of causal relationships along with the complete \
sentence/paragraph from the text that is representative of this relationship. Note that it is okay if the sentence/paragraph contains references to other variables. It is important to \
provide the complete sentence/paragraph.

Example of user input:
Text:
[provided text]
Relationships:
[provided relationships]
Similar Variables:
[provided tuples of similar variables]

Corresponding JSON output:
{
    "Step 1": {"pairs":[
        {"tuple": "(var1,var2)", "new_name": "[The new variable name]", "reasoning": "[Reasoning for choosing the new variable name]"},
        {"tuple": "(var3,var4)", "new_name": "[The new variable name]", "reasoning": "[Reasoning for choosing the new variable name]"},
        {"tuple": "(var5,var6)", "new_name": "[The new variable name]", "reasoning": "[Reasoning for choosing the new variable name]"},
        ...],
        "Updated Causal Relationships": "[The updated causal relationships as a string]"
        }
    "Step 2": {"Final Relationships": [
        {"relationship": "[first relationship]", "relevant text": "[The full sentence/paragraph that the relationship represents]", "reasoning": "[your reasoning for this causal relationship]"},
        {"relationship": "[second relationship]", "relevant text": "[The full sentence/paragraph that the relationship represents]", "reasoning": "[your reasoning for this causal relationship]"},
        {"relationship": "[third relationship]", "relevant text": "[The full sentence/paragraph that the relationship represents]", "reasoning": "[your reasoning for this causal relationship]"},
        ...],
        "comments": "[write any comments or doubts you may have about the entire process here]"
    }

Please ensure that you follow the above JSON output format."""}]

        prompt = f"""
        Text:
        {text}
        Relationships:
        {lines}
        Similar Variables:
        {similar_variables}"""

        context.append({'role': 'user', 'content':prompt})
        corrected_response = get_completion_from_messages(context)
        corrected_response = get_json(corrected_response)
        relationships = corrected_response["Step 2"]["Final Relationships"]
        if self.verbose:
            merges = corrected_response["Step 1"]["pairs"]
            for line in merges:
                vars = re.findall(r'\b[\w\s]+\b', line["tuple"])
                reason = line["reasoning"]
                name = line["new_name"]
                print(DARK_GREEN+f"Merging {vars[0].lower()} & {vars[1].lower()}..."+RESET)
                print(DARK_GREEN+f"Choosing the new variable name: {name.lower()}"+RESET)
                print(DARK_GREEN+f"Reason: {reason}"+RESET)

        new_lines = []
        for line in relationships:
            relevant_txt = self.get_line(line["relevant text"])
            lines_tuple = (line["relationship"].lower(),line["reasoning"], relevant_txt)
            new_lines.append(lines_tuple)
        return new_lines