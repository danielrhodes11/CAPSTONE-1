// document.addEventListener('DOMContentLoaded', function () {
//     const container = document.querySelector('#searchResultsContainer');
//     if (!container) {
//         console.error("Container not found. Check your HTML structure.");
//         return;
//     }

//     let offset = 0; // Initial offset
//     const songName = container.getAttribute('data-song-name'); // Get the song name from data attribute
//     const playlistId = container.getAttribute('data-playlist-id'); // Get the playlist ID from data attribute

//     if (!songName) {
//         console.error("Data attribute 'data-song-name' is missing or empty.");
//         return;
//     }

//     const infScroll = new InfiniteScroll(container, {
//         // Customize your options here
//         path: function () {
//             // Construct the URL for loading more results based on whether it's a global search or playlist-specific search
//             if (playlistId) {
//                 // If there's a playlist ID, it's a playlist-specific search
//                 return `/playlists/${playlistId}/load_more_search_results?song_name=${songName}&offset=${offset}`;
//             } else {
//                 // Otherwise, it's a global search
//                 return `/load_more_search_results?song_name=${songName}&offset=${offset}`;
//             }
//         },
//         append: '.list-group-item', // Selector for the items to append
//         history: false, // Set to true if you want to use browser history
//         status: '.page-load-status', // Selector for the loading status element
//         debug: false, // Set to true for debugging
//     });

//     infScroll.on('load', function (response) {
//         // Handle the loaded content here, similar to the previous JavaScript code
//         // Update the offset
//         offset += response.items.length;
//     });

//     console.log('Song Name:', songName);
//     console.log('Offset:', offset);
//     console.log('Playlist ID:', playlistId);
// });
