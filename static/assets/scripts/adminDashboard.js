console.log($)
dashboardcontent = document.getElementById("dashboardcontent")
$("#upload-movie-button").on("click", function(){
    dashboardcontent.innerHTML = `
    <form action="/uploadMovie" method="post" class="form" enctype="multipart/form-data">
    <div class="form-group">
        <label>Image</label>
        <input type="file" class="form-control" name="image">
    </div>
    <div class="form-group">
        <label>Title</label>
        <input type="text" name="title" class="form-control">
        
    </div>
    <div class="form-group">
        <label>Genre</label>
        <input type="text" name="genre" class="form-control">
    </div>
    <div class="form-group">
        <label>Description</label>
        <textarea name="description" class="form-control"></textarea>
    </div>
    <div class="form-group">
        <label>Movie</label>
        <input type="file" class="form-control">
    </div>
    <button class="btn btn-dark">Upload</button>
</form>
    `
})

$("#view-movies-button").on("click", function(){
    $.ajax({
        url: "/get-movies",
        type: "GET",
        success: function(data) {
            console.log(data);
            let dashboardContent = data.map(each_item => {
            return `
            <div>
                    <div class="card" style="width: 300px;">                        
                        <div style="width: 100%; height: 300px; display: flex; justify-content: center; align-items: center; border: 1px solid #00c8bf;">movie image</div>
                        <div class="card-body">
                            <div class="card-title" style="display: flex; justify-content: space-between; align-items: center;">
                                <h5>${each_item.title}</h5>
                                <button class="btn btn-sm btn-outline-danger">delete</delete>
                            </div>
                            <small class="text-muted">${each_item.genre}</small>
                            <p class="card-text">${each_item.description}</p>
                        </div>
                    </div>
                    
                </div>
            `;
    }).join('');
    document.getElementById("dashboardcontent").innerHTML = `<div style="display: flex; flex-wrap: wrap; gap: 20px;">${dashboardContent}</div>`
        },
        error: function() {
            console.log("Error occurred while fetching movies.");
        }
    });
    
    // let dashboardContent = movieStore.map(each_item => {
    //     return `
    //        <div>
    //             <div class="card" style="width: 300px;">
    //                 <img src="${each_item.imgSrc}" class="card-img-top" style="width: 100%; height: 300px">
    //                 <div class="card-body">
    //                     <h5 class="card-title">${each_item.title}</h5>
    //                     <small class="text-muted">${each_item.genre}</small>
    //                     <p class="card-text">${each_item.description}</p>
    //                 </div>
    //             </div>
    //         </div>
    //     `;
    // }).join('');
    // document.getElementById("dashboardcontent").innerHTML = `<div style="display: flex; flex-wrap: wrap; gap: 20px;">${dashboardContent}</div>`
})










