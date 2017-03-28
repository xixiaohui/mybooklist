

window.onload = function(){

	// alert("i am frank");

	var cut = document.getElementById("cut");

	// alert(cut);

	var scissor = document.getElementById("scissor");


	cut.onclick = function(){
		// alert("thanks for clicking me!");
		scissor.parentNode.removeChild(scissor);
	};

}

