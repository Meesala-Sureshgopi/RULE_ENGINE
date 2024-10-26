// Function to create a rule
function createRule() {
    const rule = document.getElementById('rule').value;
    fetch('/create_rule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rule }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('output').innerText = data.message;
        loadRules();  // Reload the rules list
    })
    .catch(error => {
        console.error('Error creating rule:', error);
        document.getElementById('output').innerText = 'Error creating rule';
    });
}

// Function to combine rules
function combineRules() {
    const rule_ids = document.getElementById('rule_ids').value.split(',').map(id => id.trim());
    fetch('/combine_rules', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rule_ids }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('output').innerText = data.message;
        loadRules();  // Reload the rules list
    })
    .catch(error => {
        console.error('Error combining rules:', error);
        document.getElementById('output').innerText = 'Error combining rules';
    });
}

// Function to evaluate a rule
function evaluateRule() {
    const rule_id = document.getElementById('rule_id').value;
    const data = JSON.parse(document.getElementById('data').value);
    fetch('/evaluate_rule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rule_id, data }),
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            document.getElementById('evaluation_results').innerText = result.error;
        } else {
            document.getElementById('evaluation_results').innerText = `Evaluation Results: ${result.result}`;
        }
    })
    .catch(error => {
        console.error('Error evaluating rule:', error);
        document.getElementById('evaluation_results').innerText = 'Error evaluating rule';
    });
}

// Function to load and display all rules from the database
function loadRules() {
    fetch('/get_all_rules')
    .then(response => response.json())
    .then(data => {
        const rulesList = document.getElementById('rules_list');
        rulesList.innerHTML = '';
        data.rules.forEach(rule => {
            const li = document.createElement('li');
            li.innerText = `ID: ${rule.id} - ${rule.rule}`;
            rulesList.appendChild(li);
        });
    })
    .catch(error => {
        console.error('Error loading rules:', error);
        document.getElementById('rules_list').innerText = 'Error loading rules';
    });
}

// Load rules when the page loads
window.onload = loadRules;
