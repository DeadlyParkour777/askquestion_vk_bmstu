function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function vote(type, id, value) {
    const formData = new FormData();
    formData.append(type === 'question' ? 'question_id' : 'answer_id', id);
    formData.append('value', value);

    fetch(`/vote/${type}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.rating !== undefined) {
            const counter = document.getElementById(`${type}-rating-${id}`);
            if (counter) counter.innerText = data.rating;
        } else if (data.error) {
            alert(data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}

function markCorrect(answerId) {
    const formData = new FormData();
    formData.append('answer_id', answerId);

    fetch('/correct/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'ok') {
            document.querySelectorAll('.correct-checkbox').forEach(cb => cb.checked = false);
            document.getElementById(`correct-${answerId}`).checked = true;
        } else if (data.error) {
            alert(data.error);
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    
    document.querySelectorAll('.vote-question').forEach(btn => {
        btn.addEventListener('click', function() {
            vote('question', this.dataset.id, this.dataset.value);
        });
    });

    document.querySelectorAll('.vote-answer').forEach(btn => {
        btn.addEventListener('click', function() {
            vote('answer', this.dataset.id, this.dataset.value);
        });
    });

    document.querySelectorAll('.correct-checkbox').forEach(chk => {
        chk.addEventListener('change', function() {
            markCorrect(this.dataset.id);
        });
    });
});
