document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.like').forEach(button => {
      button.onclick = function() {
          console.log(this.dataset.post);
          console.log(this.dataset.type);
          const id = this.dataset.post 
          const type = this.dataset.type

          fetch(`/like/${id}/${type}`, {
            method: 'POST',
            body: JSON.stringify({
            })
          });
          
          location.reload(true)
      };
  });
})

document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.unlike').forEach(button => {
      button.onclick = function() {
          console.log(this.dataset.post);
          console.log(this.dataset.type);
          const id = this.dataset.post 
          const type = this.dataset.type

          fetch(`/unlike/${id}/${type}`, {
            method: 'POST',
            body: JSON.stringify({
            })
          });

          location.reload(true)
      };
  });
})