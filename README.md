# Rule Engine with AST

A 3-tier application designed to determine user eligibility based on various attributes (e.g., age, department, income, etc.). The engine dynamically creates, combines, and modifies conditional rules using an Abstract Syntax Tree (AST), making it highly flexible and efficient.

## Objective

The Rule Engine evaluates eligibility based on rules created and stored in AST format, allowing users to create, combine, and evaluate complex conditions. 

## Features
- **Rule Creation**: Define custom eligibility rules as conditions (e.g., `age > 30 AND department = 'Sales'`).
- **AST Representation**: Convert rules into an AST structure, which improves flexibility and rule modification.
- **Rule Combination**: Merge multiple rules efficiently using optimized heuristics.
- **Rule Evaluation**: Use JSON data to evaluate the rule conditions and get eligibility results.
- **Error Handling**: Handles invalid rules and checks for missing attributes.


### Database
Uses Firebase to store rule ASTs and metadata. The configuration file "database.json"

### API Functions
1. **create_rule(rule_string)**: Converts a rule string (e.g., `age > 30 `) into an AST structure.
2. **combine_rules(rules)**: Combines multiple ASTs into a single AST using efficient strategies.
3. **evaluate_rule(JSON data)**: Checks if data (e.g., `{"age": 35}`) meets eligibility criteria based on the rules.

## RUNNING THE APPLICATION

1. **Clone the repository**:

   git clone https://github.com/Meesala-Sureshgopi/Rule_Engine.git
   
   cd Rule_Engine
   

3. **Setup Environment**:
   - Install dependencies with `pip install -r requirements.txt`.
   - Configure Firebase in `config/database.json`.

4. **Running the Application**:
   
    Create and Activate a virtual environment.

     python -m venv venv  
     .\venv\Scripts\activate

5.  **Running the Application**:
   
      python app.py 
  

6. **Usage**:
   
   Based on requirements create, combine, and evaluate rules with JSON data.
