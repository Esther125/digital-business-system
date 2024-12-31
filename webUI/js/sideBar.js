var frame3,pageHead,pageTail,aside,openSidebarButton,closeSidebarButton;

function initializeElements(){
    frame3 = document.getElementById("frame-3");
    pageHead = document.getElementById("page-head");
    pageTail = document.getElementById("page-tail");
    aside = document.getElementById("aside");
    openSidebarButton = document.getElementById("openSidebarButton");
    closeSidebarButton = document.getElementById("closeSidebarButton");
    setupEventListeners();
}
function setupEventListeners() {
     // <aside> 的點擊事件
     openSidebarButton.addEventListener("click",openSidebar);
     closeSidebarButton.addEventListener("click",closeSidebar);

}
// 開啟/關閉 <aside>
function openSidebar() {
    frame3.setAttribute("class","frame-3-right");
    pageHead.setAttribute("class","page-head-right");
    pageTail.setAttribute("class","page-tail-right");
    aside.setAttribute("class","aside-left");
    openSidebarButton.setAttribute("class","index-invisable");
    console.log("open");
  }

  function closeSidebar() {
    frame3.setAttribute("class","frame-3");
    pageHead.setAttribute("class","page-head");
    pageTail.setAttribute("class","page-tail");
    aside.setAttribute("class","aside");
    openSidebarButton.setAttribute("class","index");
    console.log("close");
  }
  // 瀏覽器載入時呼叫
document.addEventListener('DOMContentLoaded', initializeElements);