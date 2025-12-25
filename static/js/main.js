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

    const url = type === 'question' ? '/vote/question/' : '/vote/answer/';

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: formData
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
            return null; 
        }
        if (!response.ok) {
             return response.json().then(err => { throw new Error(err.error || 'Ошибка сервера'); });
        }
        return response.json();
    })
    .then(data => {
        if (!data) return; 

        if (data.rating !== undefined) {
            document.getElementById(`${type}-rating-${id}`).innerText = data.rating;
        } 
    })
    .catch(error => {
        console.error('Error:', error);
        alert(error.message);
    });
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
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
            return null;
        }
        return response.json();
    })
    .then(data => {
        if (!data) return;

        if (data.status === 'ok') {
            document.querySelectorAll('.correct-checkbox').forEach(cb => cb.checked = false);
            document.getElementById(`correct-${answerId}`).checked = true;
        } else if (data.error) {
            alert(data.error);
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const attachVoteEvents = (selector, type) => {
        document.querySelectorAll(selector).forEach(btn => {
            btn.style.cursor = 'pointer'; 
            btn.onclick = function() {
                vote(type, this.dataset.id, this.dataset.value);
            };
        });
    };

    attachVoteEvents('.vote-question', 'question');
    attachVoteEvents('.vote-answer', 'answer');

    document.querySelectorAll('.correct-checkbox').forEach(chk => {
        chk.style.cursor = 'pointer';
        chk.addEventListener('change', function() {
            markCorrect(this.dataset.id);
        });
    });
});
