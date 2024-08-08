import json

# 加载 workshopData-1.json 数据
with open('workshopData-1.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
# 加载 AgentList.json 数据
with open('AgentList.json', 'r', encoding='utf-8') as file:
    agent_data = json.load(file)


# 访问 'ionic' 部分的 'Event'
ionic_events = data['ionic'][0]['Event']    
# 提取 "ionic" 部分的特定信息
for workshop_name, workshops in data.items():
    if workshop_name == "ionic":  # Check if the workshop name is 'ionic'
        for workshop_details in workshops:
            # Extracting details for the 'ionic' workshop
            date = workshop_details['Date']
            pnum = workshop_details['PNum']
            location = workshop_details['Location']
            
            # Display the extracted information for the 'ionic' workshop
            print(f"Workshop: {workshop_name}, Date: {date}, PNum: {pnum}, Location: {location}")

# 首先展示所有事件供用户选择
print("Available Events:")
event_options = {i+1: event['EventName'] for i, event in enumerate(ionic_events)}
for option, event_name in event_options.items():
    print(f"{option}. {event_name}")
try:
    # 获取用户选择的事件
    event_choice = int(input("\nEnter the number of the event you choose: "))
    selected_event = ionic_events[event_choice - 1]  # 用户输入的数字对应列表索引需减1

    # 现在展示用户选择的事件下的活动列表
    activity_list = selected_event.get('ActivityList', [])  # 避免 KeyError，使用默认空列表
    if activity_list:
        print("\nAvailable Activities:")
        activity_options = {i+1: activity['Activity'] for i, activity in enumerate(activity_list)}
        for option, activity in activity_options.items():
            print(f"{option}. {activity}")

        # 获取用户选择的活动
        activity_choice = int(input("Enter your choice of activity (number): "))
        selected_activity = activity_options.get(activity_choice)
        if selected_activity:
            print(f"\nYou have selected: {selected_activity}")
        else:
            print("\nInvalid choice, please enter a valid number.")
    else:
        print("\nNo activities available for this event.")

except ValueError:
    print("\nPlease enter a valid number for your choices.")
except IndexError:
    print("\nInvalid event choice, please enter a valid number from the event list.")

# 假设 user_selected_trigger 是用户选择的活动中的 trigger 值
#user_selected_trigger = "某个触发器值"  # 这应该是从用户选择的活动中获取的实际值
user_selected_trigger = selected_event['Trigger']

# 查找并呼叫匹配的角色
def find_and_call_agent(trigger, agent_data):
    for role, details in agent_data.items():
        for detail in details:
            if trigger in detail['tag']:
                return role
    return None

# 使用用户选择的 trigger 来找到对应的角色
matched_role = find_and_call_agent(user_selected_trigger, agent_data)

if matched_role:
    print(f"Calling the role: {matched_role}")
else:
    print("No matching role found for the trigger.")
