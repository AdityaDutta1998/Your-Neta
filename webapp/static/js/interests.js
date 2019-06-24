var state = localStorage.getItem('state');
var constituency = localStorage.getItem('constituency');

if (state == null || constituency == null){
  var base_url = window.location.origin;
	location.href = base_url+"/";
}

function validate(){
  var arr = [];

  if(document.getElementById('int_emp').checked){
    arr.push('Employment');
  }
  if(document.getElementById('int_health').checked){
    arr.push('Health');
  }
  if(document.getElementById('int_infra').checked){
    arr.push('Infrastructure');
  }
  if(document.getElementById('int_safety').checked){
    arr.push('Safety');
  }
  if(document.getElementById('int_edu').checked){
    arr.push('Education');
  }
  if(document.getElementById('int_rel').checked){
    arr.push('Religion');
  }
  if(document.getElementById('int_agri').checked){
    arr.push('Agriculture');
  }
  if(document.getElementById('int_dev').checked){
    arr.push('Development');
  }
  if(document.getElementById('int_corr').checked){
    arr.push('Corruption');
  }
  if(document.getElementById('int_trans').checked){
    arr.push('Transportation');
  }

  if(arr.length <= 0){
    $("#error_header").show();
    $("#error_header").text("Please select atleast one property");
    return;
  }


  localStorage.setItem('categories', JSON.stringify(arr));

  var base_url = window.location.origin;
	location.href = base_url+"/mp";
}

