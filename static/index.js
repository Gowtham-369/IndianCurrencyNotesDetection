let englishtext = "";
let hinditext = "";

// No need of progress bar for time delay in app version-2 but kept it due to nice animation.

window.onload = () => {
	$('#sendbutton').click(() => {
		englishtext = "";
		hinditext = "";
		hideInterface();

		imagebox = $('#imagebox')
		input = $('#imageinput')[0]
		if(input.files && input.files[0])
		{
			let formData = new FormData();
			formData.append('image' , input.files[0]);
			$.ajax({
				url: "http://192.168.8.112:8080/detectObject", 
				// fix below to your liking
				// url: "http://xxx.xxx.xxx.xxx:8080/detectObject", 
				type:"POST",
				data: formData,
				cache: false,
				processData:false,
				contentType:false,
				error: function(data){
					console.log("upload error" , data);
					console.log(data.getAllResponseHeaders());

					updateInterface();
				},
				success: function(data){
					console.log(data);
					bytestring = data['status'];
					image = bytestring.split('\'')[1];
					englishtext = data['englishmessage'];
					hinditext = data['hindimessage'];
					imagebox.attr('src' , 'data:image/jpeg;base64,'+image);
					
					// $('#audio').html('<audio autoplay><source src="static/detected_image.mp3"></audio>');
					updateInterface();					
				}
			});
			
		}
	});

	// below speechSynthesis WebAPI
	const voiceEnglishOutputButton = document.getElementById('voice-english-output');
	const voiceHindiOutputButton = document.getElementById('voice-hindi-output');
	voiceEnglishOutputButton.addEventListener('click', () => {
		let utterance = new SpeechSynthesisUtterance(englishtext);
		// utterance.lang = "en-US";
		utterance.lang = "en-GB";
		// utterance.voice = speechSynthesis.getVoices()[2]; // MS Zira
		// utterance.voice = speechSynthesis.getVoices()[4]; // Google English
		utterance.voice = speechSynthesis.getVoices()[5];// Google English Female
		speechSynthesis.speak(utterance);
	});
	voiceHindiOutputButton.addEventListener('click', () => {
		let utterance = new SpeechSynthesisUtterance(hinditext);
		utterance.lang = "hi-IN";
		utterance.voice = speechSynthesis.getVoices()[10];// Google Hindi Female
		speechSynthesis.speak(utterance);
	});
};



function readUrl(input){
	imagebox = $('#imagebox');
	console.log("evoked readUrl");
	if(input.files && input.files[0]){
		let reader = new FileReader();
		reader.onload = function(e){
			// console.log(e)
			
			imagebox.attr('src',e.target.result); 
			//change image dimensions
			resizeImage();
		}
		reader.readAsDataURL(input.files[0]);
	}
}

function myResizeFunction2(y){
	if (y.matches) {
		imagebox.width(640);
		imagebox.height(640);
		// appName = $('.title-wrap');
		// appName.css({"font-size": "35px !important"}); //not working as expected
	}
	else {
		imagebox.width(940);
		imagebox.height(740);
		// appName = $('.title-wrap');
		// appName.css({"font-size": "50px !important"}) ; //not working
		// appName.style.fontSize = "50px"; // not working
	}
}
function myResizeFunction1(x) {
	imagebox = $('#imagebox');
	
	if(x.matches){
		imagebox.width(360);
		imagebox.height(360);
		// appName = $('.title-wrap');
		// appName.css({"font-size": "25px !important"})
	}
	else{ 
		let y = window.matchMedia("(max-width:1050px)");
		myResizeFunction2(y);
		y.addListener(myResizeFunction2);//attach event listener on every change
	}
}
function resizeImage(){
	
	let x = window.matchMedia("(max-width:700px)");
	myResizeFunction1(x);
	x.addListener(myResizeFunction1);
	
}

function hideInterface(){
	$(".loading").hide();
	let progresstext = document.querySelector('.text');
	progresstext.style.display = "none";//hide completed text
	hideButtons();
	function hideButtons(){
		$("#voice-english-output").hide();
		$("#voice-hindi-output").hide();
	}
}

function updateInterface(){
	$(".loading").show();
	progress();

	// show voice output after 18s approx
	setTimeout(
		function () {
			showTarget();
		}, 10000
	);

	function showTarget() {
		$("#voice-english-output").show();
		$("#voice-hindi-output").show();
	}
}

function progress() {
	let percent = document.querySelector('.percent');
	let progress = document.querySelector('.progress');
	let text = document.querySelector('.text');
	let count = 12;//4
	let per = 8;//16
	let loading = setInterval(animateProgress, 100);

	function animateProgress() {
		if (count == 100 && per == 360) {
			percent.classList.add("text-blink")
			percent.innerText = "Audio File Generated!! Click Get Speech Out"
			percent.style.fontSize = "20px";

			text.style.display = "block";
			clearInterval(loading);
		}
		else {
			per = per + 4;
			count = count + 1;
			progress.style.width = per + 'px';
			// percent.textContent = count + '%';
			percent.innerText = count + '%';
		}
	}
}

function changeColor(){
	let sendButton = document.querySelector("#sendbutton");
	// let sendButton = document.getElementById("sendbutton");
	sendButton.style.backgroundColor = "orange";
	sendButton.style.color = "black";
}