var state = localStorage.getItem('state');
var constituency = localStorage.getItem('constituency');
var categories = JSON.parse(localStorage.getItem('categories'));



if (state == null || constituency == null || categories == null){
  var base_url = window.location.origin;
	location.href = base_url+"/";
}

$.get("/get_mp_rating",{
    state: state,
    constituency: constituency,
    categories: JSON.stringify(categories)
    }, function(data, status){

      document.getElementById('mp_loading').style.display = "none";

      if(data.error){
        document.getElementById('mp_info').style.display = "none";
        document.getElementById('mp_no_info').style.display = "block";
        return;
      }

      if(data.image){
        document.getElementById('mp_img').src = data.image;  
      }
      
      document.getElementById('mp_info').style.display = "block";
      document.getElementById('name').textContent= data.mp_name;

     
      for(i=0; i<data.score.length;  i++){
        var interest = data.score[i].category.toLowerCase()
        var score = data.score[i].score;

        var div = document.getElementById('checkbox_div'+i);
        var id = 'mp_checkbox_'+interest;

        var checkbox = document.createElement('input');
        checkbox.type = "checkbox";
        checkbox.id = id;
        checkbox.disabled = true;

        var label = document.createElement('label');
        label.htmlFor =id; 
        label.innerHTML = data.score[i].category;
        
        if(score>0){
          checkbox.checked = true
        }

        div.appendChild(checkbox);
        div.appendChild(label);    
        
      }


    });
