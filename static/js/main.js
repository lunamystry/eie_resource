// // Require the module we just created
// require(["eie/eg"], function(myModule){
//   // Use our module to change the text in the greeting
//   myModule.setText("greeting", "Hello Dojo!");

//   // After a few seconds, restore the text to its original state
//   setTimeout(function(){
//     myModule.restoreText("greeting");
//   }, 3000);
// });
// var dojoConfig = {
//   async: true,
//   // This code registers the correct location of the "demo"
//   // package so we can load Dojo from the CDN whilst still
//   // being able to load local modules
//   packages: [{
//     name: "js",
//     location: location.pathname.replace(/\/[^/]*$/, '')}]
// };

require(["dojo/fx", "dojo/dom", "eie/eg", "dojo/domReady!"], function(fx,dom,eg){
  var greeting = dom.byId("greeting");
  greeting.innerHTML += " Hello from Dojo!";

  eg.setText("greeting", "Hello Dojo!");
  setTimeout(function(){
    eg.restoreText("greeting");
  }, 500)

  fx.slideTo({
    top: 100,
    left: 200,
    node: greeting
  }).play();
});
