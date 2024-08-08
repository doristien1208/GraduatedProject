import json
from openai import OpenAI


# 引入openAI api_key
client = OpenAI(api_key='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')

# read workshopData-1.json 
with open('./workshopData-1.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
# read AgentList.json 
with open('./AgentList.json', 'r', encoding='utf-8') as file:
    agent_data = json.load(file)

def display_workshops(data):
    print("Available Workshops:")
    workshops = {i+1: workshop_name for i, workshop_name in enumerate(data.keys())}
    for option, workshop_name in workshops.items():
        print(f"{option}. {workshop_name}")
    workshop_choice = int(input("\nEnter the number of the workshop you choose: "))
    workshop_name = list(data.keys())[workshop_choice - 1]
    return display_workshop_info(data, workshop_name)

def display_workshop_info(data, workshop_name):
    workshops = data[workshop_name]
    for workshop_details in workshops:
        date = workshop_details['Date']
        pnum = workshop_details['PNum']
        location = workshop_details['Location']
        print(f"Workshop: {workshop_name}, Date: {date}, PNum: {pnum}, Location: {location}")
    return workshops[0]['Event']

def choose_event(events):
    print("\nAvailable Events:")
    event_options = {i+1: event['EventName'] for i, event in enumerate(events)}
    for option, event_name in event_options.items():
        print(f"{option}. {event_name}")
    event_choice = int(input("\nEnter the number of the event you choose: "))
    return events[event_choice - 1]

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
    matched_role = []
    # 確保triggers是列表形式
    if not isinstance(trigger, list):
        trigger = [trigger]
    
    for trigger in trigger:
        for role, details in agent_data.items():
            for detail in details:
                if 'tag' in detail and (trigger in detail['tag'] if isinstance(detail['tag'], list) else trigger == detail['tag']):
                    if role not in matched_role:  # 避免重複角色
                        matched_role.append(role)
    return matched_role

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

def generate_character_descriptions_with_openai(roles, agent_data, client):
    descriptions = {}
    for role in roles:
        character_traits = get_character_traits_for_role(agent_data, role)
        if character_traits:  # 確保找到角色資料
            prompt = f"Write a detailed character prompt for a {character_traits['occupation']} with {character_traits['personality']} personality, skilled in {character_traits['skills']}. The character should be involved in {character_traits['scenario']}."
            chat_completion = client.chat.completions.create(
               messages=[
                {
                    "role":"user",
                    "content": prompt
                }    
            ],
            model="gpt-4-turbo-preview"
            )
            # 將生成的內容放到descriptions
            descriptions[role] = chat_completion.choices[0].message.content
        else:
            descriptions[role] = "Character traits not found."
    return descriptions

def role_play_conversation(role_description, client):
    print("\nStarting role-play conversation. Type 'quit' to exit.")
    
    #目前抓取名稱功能無效，會顯示為unknow role
    # 尝试提取角色名字，假设格式为"Name: 名字"
    name_prefix = "Name: "
    start_index = role_description.find(name_prefix)
    if start_index != -1:
        start_index += len(name_prefix)
        end_index = role_description.find("\n", start_index)  # 假设名字后跟换行符
        if end_index == -1:
            end_index = len(role_description)  # 如果没有换行符，取整个字符串的剩余部分
        role_name = role_description[start_index:end_index].strip()
    else:
        role_name = "Unknown Role"  # 如果找不到名字，使用默认值
    
    # 初始消息，设置角色的背景
    messages = [
        {
            "role": "system",
            "content": f"Imagine you are a {role_description}. You respond to questions and interact based on this personality and background."
        },
        {
            "role": "user",
            "content": "Hello!"
        }
    ]
    
    # 用于持续对话直至用户选择退出
    while True:
        input_message = input("You: ")
        if input_message.lower() == 'quit':
            print("Exiting role-play conversation.")
            break
        messages.append({"role": "user", "content": input_message})
        
        # 调用 OpenAI API 发送消息并获取回复
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="gpt-4-turbo-preview",  # 确保使用的模型正确
            max_tokens=150  # 你可以根据需要调整最大回复长度
        )
        
        # 提取并打印模型的回复
        reply = chat_completion.choices[0].message.content
        print(f"{role_name}: {reply}")
        # 将模型的回复加入消息列表，以维持对话上下文
        messages.append({"role": "assistant", "content": reply})

# main program
try:
    events = display_workshops(data)
    selected_event = choose_event(events)
    user_selected_trigger = choose_activity(selected_event)
    matched_role = find_and_call_agent(user_selected_trigger, agent_data)
    if matched_role:
        print(f"Calling the role: {matched_role}")
    else:
        print("No matching role found for the trigger.")
except ValueError:
    print("\nPlease enter a valid number for your choices.")
except IndexError:
    print("\nInvalid choice, please enter a valid number from the list.")

#descriptions = generate_character_descriptions_with_openai(matched_role, agent_data, client)
#for role, description in descriptions.items():
#    print(f"\nI want you to act like {role}: {description}")

descriptions = generate_character_descriptions_with_openai(matched_role, agent_data, client)
for role, description in descriptions.items():
    print(f"\nGenerated description for {role}: {description}")
    # 使用生成的角色描述启动对话
    if input(f"Do you want to start a conversation with {role}? (yes/no): ").lower() == 'yes':
        role_play_conversation(description, client)
    
#character_traits = get_character_traits_for_role(agent_data, role)   
#prompt = f"Write a detailed character prompt for a {character_traits['occupation']} with {character_traits['personality']} personality, skilled in {character_traits['skills']}. The character should be involved in {character_traits['scenario']}."
#description = generate_character_description_with_openai(prompt)
#print(description)
