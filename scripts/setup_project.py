"""Create or reconcile the Unit 3 GitHub Project using the owner's saved login.

The token stays in process memory. No global Git or gh account is switched.
"""
from pathlib import Path
import json
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OWNER = 'chasimarshad-bot'
TITLE = 'RetainWise · Unit 3 delivery'


def query(document, variables=None):
    request = urllib.request.Request('https://api.github.com/graphql',
        data=json.dumps({'query': document, 'variables': variables or {}}).encode(),
        headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.load(response)
    if result.get('errors'):
        raise RuntimeError(json.dumps(result['errors']))
    return result['data']


if __name__ == '__main__':
    TOKEN = subprocess.check_output(['gh', 'auth', 'token', '--user', OWNER], text=True).strip()
    identity = query('query { viewer { login id } }')['viewer']
    if identity['login'] != OWNER:
        raise SystemExit('Unexpected GitHub identity')
    existing = query('query($login:String!) { user(login:$login) { projectsV2(first:50) { nodes { id title url number } } } }', {'login': OWNER})['user']['projectsV2']['nodes']
    project = next((p for p in existing if p['title'] == TITLE), None)
    if project is None:
        project = query('mutation($owner:ID!,$title:String!) { createProjectV2(input:{ownerId:$owner,title:$title}) { projectV2 { id title url number } } }', {'owner': identity['id'], 'title': TITLE})['createProjectV2']['projectV2']
    pid = project['id']
    repo = query('query { repository(owner:"chasimarshad-bot", name:"RetainWise-Employee-Attrition-Insights") { id } }')['repository']['id']
    query('mutation($p:ID!,$r:ID!) { linkProjectV2ToRepository(input:{projectId:$p,repositoryId:$r}) { repository { id } } }', {'p': pid, 'r': repo})
    fields = query('query($p:ID!) { node(id:$p) { ... on ProjectV2 { fields(first:30) { nodes { ... on ProjectV2SingleSelectField { id name options { id name } } } } } } }', {'p': pid})['node']['fields']['nodes']
    status = next(f for f in fields if f.get('name') == 'Status')
    opts = [{'name': name, 'description': '', 'color': color} for name, color in [('Todo', 'GRAY'), ('In Progress', 'YELLOW'), ('Done', 'GREEN'), ('Not Planned', 'RED')]]
    status = query('mutation($f:ID!,$o:[ProjectV2SingleSelectFieldOptionInput!]!) { updateProjectV2Field(input:{fieldId:$f,singleSelectOptions:$o}) { projectV2Field { ... on ProjectV2SingleSelectField { id name options { id name } } } } }', {'f': status['id'], 'o': opts})['updateProjectV2Field']['projectV2Field']
    priority = next((f for f in fields if f.get('name') == 'Priority'), None)
    if priority is None:
        options = [{'name': name, 'description': '', 'color': color} for name, color in [('Must Have', 'RED'), ('Should Have', 'ORANGE'), ('Could Have', 'BLUE'), ("Won't Have", 'GRAY')]]
        priority = query('mutation($p:ID!,$o:[ProjectV2SingleSelectFieldOptionInput!]!) { createProjectV2Field(input:{projectId:$p,dataType:SINGLE_SELECT,name:"Priority",singleSelectOptions:$o}) { projectV2Field { ... on ProjectV2SingleSelectField { id name options { id name } } } } }', {'p': pid, 'o': options})['createProjectV2Field']['projectV2Field']
    tasks = [
        ('Business requirements and fixed hypotheses', 'Done', 'Must Have', 'docs/PRD.md sections 6–7; notebook 03 retains H1–H4.'),
        ('Source attribution and licence verification', 'Done', 'Must Have', 'data/SOURCE.md and source_record.json record first-party Kaggle terms and acquisition.'),
        ('Execute notebooks and recreate versioned v1', 'Done', 'Must Have', 'Three fresh-kernel executions completed; outputs and metadata committed.'),
        ('Executive dashboard', 'Done', 'Must Have', 'Overview includes KPIs, rates, composition, explanations and bounded next questions.'),
        ('Pattern explorer and filter boundaries', 'Done', 'Must Have', 'Workplace and distribution views; empty and small-group handling tested.'),
        ('Hypothesis Lab and exact evidence', 'Done', 'Must Have', 'H1/H2/H4 Supported, H3 Mixed; rules and denominators shown.'),
        ('Fairness, ethics and legal context', 'Done', 'Must Have', 'Dedicated governance page; ICO guidance-under-review notice and legal sources.'),
        ('Project lifecycle and build reflection', 'Done', 'Must Have', 'Completed lifecycle and execution reflection evaluate the plan, decisions, validation and improvements. Student review remains required.'),
        ('Accessibility and responsive browser review', 'Done', 'Must Have', 'Five pages checked at 390, 768 and 1440px; automated scan returned zero selected-rule violations and four keyboard tasks passed. No formal conformance or screen-reader claim.'),
        ('Scenario-based usability checks', 'Done', 'Must Have', 'docs/user_testing.md records automated scenarios and distinguishes them from external participants.'),
        ('README and assessment evidence matrix', 'Done', 'Must Have', 'Exact artefacts linked; remaining release and student-review gates explicit.'),
        ('Final reproducibility and QA', 'Done', 'Must Have', '16 automated tests, three fresh-kernel notebooks, data-contract verification and local browser checks passed. Hosted verification belongs to the separate deployment task.'),
        ('Linux container verification', 'Done', 'Must Have', 'Pinned runtime image built; non-root health check and all five pages passed. See docs/qa/container_results.json.'),
        ('Deploy Streamlit and verify hosted app', 'Todo', 'Must Have', 'No authenticated Streamlit host session available. See docs/deployment.md; do not claim a live URL.'),
        ('Independent stakeholder feedback and student review', 'Todo', 'Should Have', 'No external participants claimed. Student must review the completed execution reflection and project evidence.'),
        ('Additional aggregate comparisons', 'Not Planned', 'Could Have', 'Deferred from the submission candidate to keep the agreed scope focused.'),
        ('Individual employee scoring and demographic targeting', 'Not Planned', "Won't Have", 'Prohibited product use; no implementation planned.'),
        ('Automated employment decisions and deep learning', 'Not Planned', "Won't Have", 'Outside the scope and responsible-use boundary.'),
    ]
    existing_items = query('query($p:ID!) { node(id:$p) { ... on ProjectV2 { items(first:100) { nodes { id content { ... on DraftIssue { id title body } } } } } } }', {'p': pid})['node']['items']['nodes']
    for title, state, prio, body in tasks:
        item = next((item for item in existing_items if (item.get('content') or {}).get('title') == title), None)
        if item is None:
            item = query('mutation($p:ID!,$t:String!,$b:String!) { addProjectV2DraftIssue(input:{projectId:$p,title:$t,body:$b}) { projectItem { id } } }', {'p': pid, 't': title, 'b': body})['addProjectV2DraftIssue']['projectItem']
        elif item['content'].get('body') != body:
            query('mutation($i:ID!,$b:String!) { updateProjectV2DraftIssue(input:{draftIssueId:$i,body:$b}) { draftIssue { id } } }', {'i': item['content']['id'], 'b': body})
        for field, value in [(status, state), (priority, prio)]:
            option = next(o['id'] for o in field['options'] if o['name'] == value)
            query('mutation($p:ID!,$i:ID!,$f:ID!,$o:String!) { updateProjectV2ItemFieldValue(input:{projectId:$p,itemId:$i,fieldId:$f,value:{singleSelectOptionId:$o}}) { projectV2Item { id } } }', {'p': pid, 'i': item['id'], 'f': field['id'], 'o': option})
    (ROOT / 'docs/project.json').write_text(json.dumps(project, indent=2), encoding='utf-8')
    print(f"Project configured: {project['url']} ({len(tasks)} scope items)")
