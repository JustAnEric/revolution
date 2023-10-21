let currDm = null
const dmPage = (dm) => {
  document.getElementById("home").hidden = true
  document.getElementById("add-a-user-panel").hidden = true
  document.getElementById("messages").hidden = false
  document.getElementById("message-input").hidden = false
  document.getElementById("user-list").hidden = false
  document.getElementById("memberListUser").textContent = user.name
  document.getElementById("message-list").innerHTML = ""
  document.getElementById("input-area").hidden = false
  document.getElementById("read-only").hidden = true
  document.getElementsByTagName("title")[0].textContent = "@" + dm.user.name + "#" + dm.user.discriminator + " | Revolution"
  //history.pushState({}, "", "https://revolution-web.repl.co/channels/@me/" + dm.id)
  channelType = "d"
  currDm = dm
  websck.send(JSON.stringify({ "type": "resetfollowlist", "token": localStorage.getItem("token") }));
  websck.send(JSON.stringify({ "type": "follow", "channels": [currDm.id.toString()], "token": localStorage.getItem("token") }));
  getDmMessages()
}
const getDmMessages = async () => {
  let loaded = false
  document.getElementById("loadingMessages").hidden = false
  document.querySelector('.channel-messages ul').innerHTML = null;

  await fetch("https://revolution-web.repl.co/get_messages/d/" + currDm.id, {
    headers: {
      amount: 20,
      skip: 0
    }
  }).then(async (response) => {
    //const body = await response.text();
    //const jsonText = body.replaceAll('\u0027', '\u0022').replaceAll(`]|sngl-qt|[`,'\'').replaceAll(']|dbl-qt|[',`'`);
    const item = await response.json() //JSON.parse(jsonText)/*.replaceAll(`'`, `"`);*/
    console.log("Got new messages")

    console.log(item)

    for (const obj of Object.entries(item)) {
      await renderMessage(obj[1])
      console.log("Rendered new messages")
    }
    const msgsDiv = document.querySelector('.channel-messages');
    document.getElementById("loadingMessages").hidden = true;
    setTimeout(() => {
      msgsDiv.scrollTop = msgsDiv.scrollHeight
      loaded = true
    }, 500);
    
    /*document.querySelector('.channel-messages ul').insertAdjacentHTML('beforeend', `<li style="padding-left: 10px; color: white; width: 100%;" onmouseover="const collection = this.children; this.style.background = '#535357'; this.style.color = 'white';" onmouseout="const collection = this.children; this.style.background = 'transparent'; this.style.color = 'white';"><b><img src="/assets/images/Goobler-meowsicles.png" width=40/> <onclickFunc onclick="">${json.message}</onclickFunc> <span class="badge" style="background: mediumpurple;">TESTER <i class="fa fa-check"></i></span> </b> <br>${json["messages"]['message']}</li>`);*/
  })
  //location.reload()
}

const sendMessageToDm = (dm) => { 
  let input = document.querySelector('#textInput');
  let channelMessages = document.querySelector('.channel-messages ul');
  if (!/[a-zA-Z]/.test(input.innerText)) {
    alert("Please add some content into your message.")
  } else {
    fetch("https://revolution-web.repl.co/send_message/d/" + currDm.id, {
      headers: {
        "message": input.innerText.replaceAll('\n','<br/>'),
        "token": localStorage.getItem("token")
      }
    }).then(function(response) {
      console.log(response)
    });
  
    input.innerText = null
  }
}
