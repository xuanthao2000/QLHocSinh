function update(classroom_id, student_id) {
    event.preventDefault()
    fetch('/classroom/update', {
            method: 'post',
            body: JSON.stringify({
            'classroom_id': classroom_id,
            'student_id': student_id,
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            if (data.code == 400)
                alert(data.err)
            if (data.code == 200)
                location.reload()
        }).catch(err =>  console.error(err))
}

function remove(classroom_id, student_id) {
    event.preventDefault()
    if (confirm('Bạn có chắc chắn muốn xóa học sinh này khỏi lớp không?') == true){
        fetch('/classroom/removeStudent', {
                method: 'post',
                body: JSON.stringify({
                'student_id': student_id,
                'classroom_id': classroom_id,
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(res => res.json()).then(data => {
                if (data.code == 200)
                    location.reload()
            }).catch(err =>  console.error(err))
    }
}