// 模拟数据
var currentStage = "創意思考";
var currentTask = "利用便條寫下創意";
var remainingTime = "15分钟";

// 更新界面数据
function updateUI() {
    document.getElementById("currentStage").textContent = currentStage;
    document.getElementById("currentTask").textContent = currentTask;
    document.getElementById("remainingTime").textContent = remainingTime;
}

// 添加用户消息到聊天框
function addUserMessage(message) {
    var chatContainer = document.getElementById("chatContainer");
    var messageElement = document.createElement("p");
    messageElement.classList.add("user-message");
    messageElement.textContent = message;
    chatContainer.appendChild(messageElement);
    chatContainer.scrollTop = chatContainer.scrollHeight; // 自动滚动到底部
}

// 添加助手消息到聊天框
function addAssistantMessage(message) {
    var chatContainer = document.getElementById("chatContainer");
    var messageElement = document.createElement("p");
    messageElement.classList.add("assistant-message");
    messageElement.textContent = message;
    chatContainer.appendChild(messageElement);
    chatContainer.scrollTop = chatContainer.scrollHeight; // 自动滚动到底部
}

// 处理用户输入
function handleUserInput() {
    var userInput = document.getElementById("userInput").value;
    addUserMessage(userInput);

    // 在这里调用 ChatGPT API 进行对话处理，并获取助手的回复
    var assistantReply = simulateAssistantReply(userInput); // 这里使用模拟的回复，你需要替换为实际的 ChatGPT API 调用

    addAssistantMessage(assistantReply);

    // 清空用户输入
    document.getElementById("userInput").value = "";
}

// 模拟助手的回复（用于演示）
function simulateAssistantReply(userInput) {
    // 在这里可以根据用户输入进行逻辑处理，然后生成助手的回复
    return "助手回复：" + userInput + " 這是一個不錯的想法！您可以試試......";
}

// 更新界面
updateUI();

// 监听用户输入框的回车键事件
document.getElementById("userInput").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        handleUserInput();
    }
});
