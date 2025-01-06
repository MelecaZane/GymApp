function getCSRFToken() {
   return document.querySelector('input[name="csrf_token"]').value;
}

function hideStartingWeight(){
    var startingWeight = document.getElementById('startingWeightBox');

     if (startingWeight.style.display === 'none'){
        startingWeight.style.display = 'block';
     } else{
        startingWeight.style.display = 'none';
     }
}

function addExerciseButton(){
   const exerciseHeadings = document.querySelectorAll('#ExerciseStorage h6');
   var exercises = [];
   exerciseHeadings.forEach(heading => {
       exercises.push([heading.id, heading.innerHTML]);
   });
   console.log(exercises);

   const newDiv = document.createElement('div');
   newDiv.classList.add('row', 'mt-3');

   const selectDiv = document.createElement('div');
   selectDiv.classList.add('col-10');

   const select = document.createElement('select');
   select.classList.add('form-select');
   select.classList.add('exercise');

   exercises.forEach(exercise => {
       const option = document.createElement('option');
       option.value = exercise[0];
       option.innerHTML = exercise[1];
       select.appendChild(option);
   });

   selectDiv.appendChild(select);

   const buttonDiv = document.createElement('div');
   buttonDiv.classList.add('col-2');

   const button = document.createElement('button');
   button.type = 'button';
   button.classList.add('btn', 'btn-danger', 'w-100');
   button.textContent = '-';
   button.onclick = function() {
       newDiv.remove();
   };

   buttonDiv.appendChild(button);

   newDiv.appendChild(selectDiv);
   newDiv.appendChild(buttonDiv);

   const form = document.querySelector('.custom-form');
   const buttonsRow = form.querySelector('.row:last-child');
   form.insertBefore(newDiv, buttonsRow);
}

function addMuscleGroupButton(){
   const muscleGroupHeadings = document.querySelectorAll('#MuscleGroupStorage h6');
   var muscleGroups = [];
   muscleGroupHeadings.forEach(heading => {
       muscleGroups.push([heading.id, heading.innerHTML]);
   });
   console.log(muscleGroups);

   const newDiv = document.createElement('div');
   newDiv.classList.add('row', 'mt-3');

   const selectDiv = document.createElement('div');
   selectDiv.classList.add('col-10');

   const select = document.createElement('select');
   select.classList.add('form-select');
   select.classList.add('group');

   muscleGroups.forEach(muscleGroup => {
       const option = document.createElement('option');
       option.value = muscleGroup[0];
       option.innerHTML = muscleGroup[1];
       select.appendChild(option);
   });

   selectDiv.appendChild(select);

   const buttonDiv = document.createElement('div');
   buttonDiv.classList.add('col-2');

   const button = document.createElement('button');
   button.type = 'button';
   button.classList.add('btn', 'btn-danger', 'w-100');
   button.textContent = '-';
   button.onclick = function() {
       newDiv.remove();
   };

   buttonDiv.appendChild(button);

   newDiv.appendChild(selectDiv);
   newDiv.appendChild(buttonDiv);

   const form = document.querySelector('.custom-form');
   const buttonsRow = form.querySelector('.row:last-child');
   form.insertBefore(newDiv, buttonsRow);
}

function submitWorkout(){
   var name = document.getElementById('workoutName').value;
   const workoutSelection = document.querySelectorAll('.form-select');
   var exercises = [];
   var groups = [];
   var order = [];
   workoutSelection.forEach(select => {
       if (select.classList.contains('exercise')){
            exercises.push(select.value);
            order.push(1);
       } else if (select.classList.contains('group')){
            groups.push(select.value);
            order.push(0);
       }
   });
   
   var xhttp = new XMLHttpRequest();
   postData = {
         'name': name,
         'exercises': exercises,
         'groups': groups,
         'order': order
   }
   xhttp.open("POST", "/addWorkout", true);
   xhttp.setRequestHeader("Content-type", "application/json");
   xhttp.setRequestHeader("X-CSRFToken", getCSRFToken());
   xhttp.send(JSON.stringify(postData));

   xhttp.onreadystatechange = function() {
      if (this.readyState == 4) {
          var response = JSON.parse(this.responseText);
          if (this.status == 200 && response.success) {
              window.location.href = response.redirect_url;
          } else {
              alert('Error: ' + response.error);
          }
      }
  }
}

function updateExercise(exerciseId){
    var data = document.getElementById(exerciseId + "-data").value;

    var xhttp = new XMLHttpRequest();
    postData = {
        'id': exerciseId,
        'data': parseFloat(data),
        'workout': document.getElementById("WorkoutStorage").innerHTML
    }
    xhttp.open("POST", "/workoutDetails/" + exerciseId, true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.setRequestHeader("X-CSRFToken", getCSRFToken());
    xhttp.send(JSON.stringify(postData));

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            var response = JSON.parse(this.responseText);
            if (this.status == 200 && response.success) {
                window.location.href = response.redirect_url;
            } else {
                alert('Error: ' + response.error);
            }
        }
    }
}