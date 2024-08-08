import json
from openai import OpenAI

# 引入openAI api_key
client = OpenAI(api_key='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')

# read workshopData-1.json 
with open('workshopData-1.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
# read AgentList.json 
with open('AgentList.json', 'r', encoding='utf-8') as file:
    agent_data = json.load(file)

def display_ionic_info(data):
    ionic_events = data['ionic'][0]['Event']
    for workshop_name, workshops in data.items():
        if workshop_name == "ionic":
            for workshop_details in workshops:
                date = workshop_details['Date']
                pnum = workshop_details['PNum']
                location = workshop_details['Location']
                print(f"Workshop: {workshop_name}, Date: {date}, PNum: {pnum}, Location: {location}")
    return ionic_events

def choose_event(ionic_events):
    print("Available Events:")
    event_options = {i+1: event['EventName'] for i, event in enumerate(ionic_events)}
    for option, event_name in event_options.items():
        print(f"{option}. {event_name}")
    event_choice = int(input("\nEnter the number of the event you choose: "))
    return ionic_events[event_choice - 1]

def choose_activity(selected_event):
    activity_list = selected_event.get('ActivityList', [])
    if activity_list:
        print("\nAvailable Activities:")
        activity_options = {i+1: activity['Activity'] for i, activity in enumerate(activity_list)}
        for option, activity in activity_options.items():
            print(f"{option}. {activity}")
        activity_choice = int(input("Enter your choice of activity (number): "))
        selected_activity = activity_options.get(activity_choice)
        if selected_activity:
            print(f"\nYou have selected: {selected_activity}")
        else:
            print("\nInvalid choice, please enter a valid number.")
    else:
        print("\nNo activities available for this event.")
    return selected_event.get('Trigger')

def find_and_call_agent(trigger, agent_data):
    for role, details in agent_data.items():
        for detail in details:
            if trigger in detail['tag']:
                return role
            
    return None

def get_character_traits_for_role(agent_data, role):
    for agent_role, details in agent_data.items():
        if agent_role.lower() == role.lower():
            for detail in details:
                # Assuming the first (or only) entry for each role contains the desired traits
                return {
                    "occupation": detail.get("occupation", ""),
                    "personality": detail.get("personality", ""),
                    "skills": detail.get("skills", ""),
                    "scenario": detail.get("scenario", "")
                }
    return {}

def generate_character_description_with_openai(prompt):
    chat_completion = client.chat.completions.create(
       messages=[
        {
            "role":"user",
            "content": prompt
        }    
    ],
    model="gpt-3.5-turbo"
    )
    return chat_completion.choices[0].message.content

# main program
ionic_events = display_ionic_info(data)
try:
    selected_event = choose_event(ionic_events)
    user_selected_trigger = choose_activity(selected_event)
    matched_role = find_and_call_agent(user_selected_trigger, agent_data)
    if matched_role:
        print(f"Calling the role: {matched_role}")
        role = matched_role     
    else:
        print("No matching role found for the trigger.")
except ValueError:
    print("\nPlease enter a valid number for your choices.")
except IndexError:
    print("\nInvalid event choice, please enter a valid number from the event list.")

#character_traits = get_character_traits_for_role(agent_data, role)   
#prompt = f"Write a detailed character prompt for a {character_traits['occupation']} with {character_traits['personality']} personality, skilled in {character_traits['skills']}. The character should be involved in {character_traits['scenario']}."
#description = generate_character_description_with_openai(prompt)
#print(description)
