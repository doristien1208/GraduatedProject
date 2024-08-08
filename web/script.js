document.getElementById("workshopForm").addEventListener("submit", function(event) {
    event.preventDefault(); // 阻止表单提交的默认行为

    var workshopTitle = document.getElementById("workshopTitle").value;

    // 生成流程模板
    var workflowTemplate = `
        <h2>工作坊流程模板</h2>
        <ul>
            <li id="workflow1">技術體驗</li>
            <li id="workflow2">創意思考</li>
            <li id="workflow3">技術方向</li>
            <li id="workflow4">點子修正與執行</li>
            <li id="workflow5">成果展現</li>
        </ul>
    `;

    document.getElementById("workflowTemplate").innerHTML = workflowTemplate;

    // 为每个流程阶段绑定点击事件
    var workflows = document.querySelectorAll("#workflowTemplate li");
    for (var i = 0; i < workflows.length; i++) {
        workflows[i].addEventListener("click", function() {
            var workflowId = this.getAttribute("id");
            var modalTitle = document.getElementById("modalTitle");
            modalTitle.textContent = workflowId;

            // 显示模态框
            document.getElementById("modal").style.display = "block";
        });
    }
});

// 保存按钮的点击事件处理程序
document.getElementById("saveButton").addEventListener("click", function() {
    // 获取填写的任务列表和时间
    var guideTasks = document.getElementById("guideTasks").value;
    var participantTasks = document.getElementById("participantTasks").value;
    var agentTasks = document.getElementById("agentTasks").value;

    // 进行相应的处理，例如保存到数据库或在页面上显示

    // 隐藏模态框
    document.getElementById("modal").style.display = "none";
});

// 取消按钮的点击事件处理程序
document.getElementById("cancelButton").addEventListener("click", function() {
    // 清除填写的任务列表和时间
    document.getElementById("guideTasks").value = "";
    document.getElementById("participantTasks").value = "";
    document.getElementById("agentTasks").value = "";

    // 隐藏模态框
    document.getElementById("modal").style.display = "none";
});
