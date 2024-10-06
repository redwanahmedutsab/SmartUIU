const responses = {
    "hello": "Hello! Welcome to SmartUIU. How can I assist you today?",
    "i am good": "Glad to hear that! How can I assist you with SmartUIU?",
    "how are you or how are you doing": "I'm doing well, thanks for asking! How can I help you?",
    "can you help me": "Of course! What would you like help with? Lost items, thesis member search, or something else?",
    "how can i sign up": "To sign up, click on 'Sign Up' and use your UIU email. Make sure to verify your account through the email verification link.",
    "how can i create an account": "To create an account, click 'Sign Up', enter your UIU email, and verify it via the link sent to your inbox.",
    "how can i search for job on this website": "Currently, SmartUIU focuses on campus-related features. You can use our platform to find events or connect with thesis members!",
    "how do i post a lost item": "To post a lost item, head over to the 'Lost and Found' section and fill out the item details. Other students will be able to contact you via phone or email.",
    "how can i remove a lost item post": "You can manage or remove your Lost and Found posts from your user dashboard under 'My Posts'.",
    "how can i find my lost item": "Go to the 'Lost and Found' section and browse all the posted items. If you find yours, contact the person via the provided details.",
    "how can i find thesis members": "To search for a thesis partner, visit the 'Thesis Member Finder' section and browse through the available profiles.",
    "how can i create or edit my thesis profile": "You can create or edit your thesis profile by visiting the 'Thesis Member Finder' section, then navigating to your dashboard.",
    "can i contact thesis members directly": "Yes, you can view profiles in the Thesis Member Finder and contact them directly through the provided contact details.",
    "how can i post an event": "To create an event, go to the 'Event Organizer' section, click 'Create Event', and fill out the details for other students to see.",
    "what types of events are posted here": "SmartUIU hosts various academic, social, and extracurricular events posted by students for the campus community.",
    "how do i rsvp to an event": "Simply click on the event you’re interested in, and hit 'RSVP' to confirm your attendance.",
    "can you help me find an event": "Of course! Go to the 'Event Organizer' section and browse through all the upcoming events listed by students.",
    "how do i edit or delete an event": "If you're the event creator, you can edit or delete it from the 'My Events' section in your dashboard.",
    "how can i create my CV": "SmartUIU doesn't have a CV creation feature yet. You can stay tuned for upcoming features like this!",
    "how do i reset my password if i forget it": "Click on 'Forgot Password' on the login page and follow the instructions to reset it.",
    "how do i edit my profile information": "You can edit your profile by clicking on 'Edit Profile' under your account settings.",
    "is there any two-factor authentication for signing in": "Currently, we don’t have two-factor authentication, but we take security seriously and encourage strong passwords.",
    "can i save events or posts to view later": "This feature isn't available yet, but we are working on providing it in future updates!",
    "what are the latest campus events": "Check the 'Event Organizer' section for the most recent and upcoming campus events.",
    "what should i do if I forget my password": "Just click on 'Forgot Password' on the sign-in page, and follow the steps to reset it.",
    "how can I report a lost item I found": "If you’ve found a lost item, go to the 'Lost and Found' section and create a post with the item details.",
    "can i collaborate on thesis projects": "Yes! You can reach out to other students through the 'Thesis Member Finder' to collaborate on research projects.",
    "how can I monitor my posts": "You can track your posts in the 'My Posts' section, where you'll see all your active and past listings.",
    "are there any upcoming events for students": "Yes, check out the 'Event Organizer' for the latest events happening on campus.",
    "how do i change my password": "You can change your password by going to 'Account Settings' and selecting 'Change Password'.",
    "what is SmartUIU used for": "SmartUIU is designed to help UIU students connect, organize events, find lost items, and collaborate on thesis projects.",
    "are there new features coming to SmartUIU": "Yes! Future updates include a Home Finder, Marketplace, and more to enhance your campus experience.",
    "who can use SmartUIU": "Only UIU students can create an account using their university email, making this platform exclusive to our community.",
    "what if I need help using SmartUIU": "If you need assistance, feel free to reach out through the 'Help' section, and we'll be happy to assist you.",
    "how can i find accommodation": "Our upcoming Home Finder feature will help you browse available housing options near campus.",
    "how do I list my home for rent": "Once the Home Finder is live, you'll be able to list your property by filling out the necessary details under the 'List Your Home' section.",
    "can i search for roommates": "The Home Finder feature will allow you to search for and connect with potential roommates once it's released.",
    "how can i buy or sell items on SmartUIU": "With the upcoming Marketplace feature, you’ll be able to buy and sell items like textbooks, gadgets, and more directly through the platform.",
    "what kind of products can i sell in the marketplace": "In the future Marketplace, you’ll be able to sell various items like books, electronics, and even clothing to fellow students.",
    "is there a fee for listing items in the marketplace": "The Marketplace feature is still under development, and we’ll announce any potential fees for listing items when it’s ready.",
    "what are the benefits of creating an account here": "By creating an account on SmartUIU, you gain access to exclusive features like the Lost & Found section, Thesis Member Finder, upcoming Home Finder, Marketplace, and personalized event recommendations. It also enables you to interact with the community and manage your own listings.",
    "can i edit my lost item post": "Yes, you can edit your lost item post from the 'My Posts' section in your dashboard.",
    "how can i contact the admin": "You can reach the admin by using the 'Contact Us' option in the Help section.",
    "what if my question isn't answered": "If you don't find your answer, you can contact support through the Help section.",
    "how do I log out": "To log out, click on your profile icon in the top right corner and select 'Log Out'.",
    "can I use SmartUIU on my mobile device": "Yes! SmartUIU is optimized for mobile devices, allowing you to access all features on the go.",
    "what happens if I violate the community guidelines": "If you violate the guidelines, your account may be suspended or banned. Please follow the rules to maintain a good standing.",
    "how do I update my profile picture": "You can update your profile picture by going to 'Edit Profile' and uploading a new image.",
    "how can I report inappropriate content": "To report inappropriate content, click on the 'Report' button next to the post or profile.",
    "what should I do if I encounter a bug": "If you encounter any issues, please report it through the Help section so we can address it promptly.",
    "can I customize my profile": "Yes! You can customize your profile by adding a bio, profile picture, and other details.",
    "will my personal information be kept safe": "Yes, we prioritize your privacy and will not share your information without your consent.",
    "what types of items can I list in the lost and found": "You can list any personal items such as books, electronics, clothing, or anything else you've lost or found.",
    "how can I improve my thesis profile visibility": "Make sure to fill out all relevant sections in your profile and use clear, concise descriptions to attract potential collaborators.",
    "what is the timeline for new features being added": "We are continuously working on improvements and aim to roll out new features regularly. Stay tuned for updates!",
    "can I invite friends to join SmartUIU": "Currently, there isn't a referral program, but you can encourage your friends to sign up and be part of our community!",
    "are there any restrictions on posting events": "Yes, all events must adhere to university guidelines and be relevant to the UIU student community.",
    "what kind of support is available if I face issues with my account": "You can reach out through the Help section for support, where we will assist you with any account-related issues.",
    "can I change my email address associated with my account": "Currently, you cannot change your email address. Please contact support for assistance if needed.",
    "is there a limit to the number of items I can post in the lost and found": "There isn't a specific limit, but please ensure your posts are relevant and necessary to maintain clarity for all users.",
    "how often are new events posted": "New events can be posted anytime by students, so check the 'Event Organizer' section frequently to stay updated.",
    "can I provide feedback on the platform": "Absolutely! We appreciate feedback and suggestions. You can submit your thoughts through the Help section.",
    "how can I keep track of events I'm interested in": "Although there isn't a current feature for saving events, we're working on implementing that in future updates.",
    "are there any plans for a mobile app": "While we currently operate as a web platform, we are considering developing a mobile app in the future for better accessibility.",
    "what should I do if I suspect a post is fraudulent": "If you encounter a suspicious post, please report it immediately through the available options next to the post.",
    "how can I stay informed about updates and new features": "You can follow our announcements in the Help section or join our mailing list to receive updates directly."
};

function toggleChatContainer() {
    const chatContainer = document.getElementById('chat-container');
    chatContainer.style.display = chatContainer.style.display === 'block' ? 'none' : 'block';
}

function longestCommonSubsequence(str1, str2) {
    const m = str1.length;
    const n = str2.length;
    const dp = new Array(m + 1).fill(null).map(() => new Array(n + 1).fill(0));

    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (str1[i - 1] === str2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    let lcs = '';
    let i = m;
    let j = n;
    while (i > 0 && j > 0) {
        if (str1[i - 1] === str2[j - 1]) {
            lcs = str1[i - 1] + lcs;
            i--;
            j--;
        } else if (dp[i - 1][j] > dp[i][j - 1]) {
            i--;
        } else {
            j--;
        }
    }

    return lcs.length;
}

const userInput = document.getElementById('user-input');
userInput.addEventListener('keyup', function (event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

// function sendMessage() {
//     const userInput = document.getElementById('user-input');
//     const chatBox = document.getElementById('chat-box');
//
//     const userMessage = userInput.value.trim();
//     if (userMessage !== '') {
//         const userMsgDiv = document.createElement('div');
//         userMsgDiv.classList.add('user-msg');
//         userMsgDiv.textContent = userMessage;
//         chatBox.appendChild(userMsgDiv);
//
//         let botMessage = "I'm sorry, I don't understand.";
//         let matchedResponse = false;
//
//         for (const query in responses) {
//             const lcsLength = longestCommonSubsequence(userMessage.toLowerCase(), query.toLowerCase());
//             const similarity = lcsLength / Math.max(userMessage.length, query.length);
//             if (similarity > 0.3) {
//                 botMessage = responses[query];
//                 matchedResponse = true;
//                 break;
//             }
//         }
//
//         setTimeout(function () {
//             const botMsgDiv = document.createElement('div');
//             botMsgDiv.classList.add('bot-msg');
//             chatBox.appendChild(botMsgDiv);
//
//             if (!matchedResponse) {
//                 botMsgDiv.textContent = "I couldn't find an exact answer. Would you like to contact a person for help?";
//
//                 // Create Yes and No buttons
//                 const yesButton = document.createElement('button');
//                 yesButton.textContent = 'Yes';
//                 yesButton.classList.add('yes-button');
//
//                 const noButton = document.createElement('button');
//                 noButton.textContent = 'No';
//                 noButton.classList.add('no-button');
//
//                 chatBox.appendChild(yesButton);
//                 chatBox.appendChild(noButton);
//
//                 // Handle Yes button click
//                 yesButton.addEventListener('click', function () {
//                     startCrispChat();
//                     botMsgDiv.textContent = "Starting the chat with a representative...";
//                     chatBox.removeChild(yesButton);
//                     chatBox.removeChild(noButton);
//                 });
//
//                 // Handle No button click
//                 noButton.addEventListener('click', function () {
//                     botMsgDiv.textContent = "Okay, feel free to ask me anything else!";
//                     chatBox.removeChild(yesButton);
//                     chatBox.removeChild(noButton);
//                 });
//
//                 chatBox.scrollTop = chatBox.scrollHeight;
//             } else {
//                 botMsgDiv.textContent = botMessage;
//             }
//
//             chatBox.scrollTop = chatBox.scrollHeight;
//         }, 500);
//
//         userInput.value = ''; // Clear input field after sending message
//     }
// }


function sendMessage() {
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');

    const userMessage = userInput.value.trim();
    if (userMessage !== '') {
        const userMsgDiv = document.createElement('div');
        userMsgDiv.classList.add('user-msg');
        userMsgDiv.textContent = userMessage;
        chatBox.appendChild(userMsgDiv);

        let bestProbability = 0;
        let bestResponse = "I'm sorry, I don't understand."; // Default message if no match is found
        let matchedResponse = false;

        for (const query in responses) {
            const lcsLength = longestCommonSubsequence(userMessage.toLowerCase(), query.toLowerCase());
            const similarity = lcsLength / Math.max(userMessage.length, query.length);

            // Check if the similarity is greater than the best probability found so far
            if (similarity > bestProbability) {
                bestProbability = similarity; // Update best probability
                bestResponse = responses[query]; // Update best response
                matchedResponse = true; // Mark that we found a matching response
            }
        }

        setTimeout(function () {
            const botMsgDiv = document.createElement('div');
            botMsgDiv.classList.add('bot-msg');
            chatBox.appendChild(botMsgDiv);

            if (!matchedResponse || bestProbability < 0.3) { // Check if there was a good match
                botMsgDiv.textContent = "I couldn't find an exact answer. Would you like to contact a person for help?";

                // Create Yes and No buttons
                const yesButton = document.createElement('button');
                yesButton.textContent = 'Yes';
                yesButton.classList.add('yes-button');

                const noButton = document.createElement('button');
                noButton.textContent = 'No';
                noButton.classList.add('no-button');

                chatBox.appendChild(yesButton);
                chatBox.appendChild(noButton);

                // Handle Yes button click
                yesButton.addEventListener('click', function () {
                    startCrispChat();
                    botMsgDiv.textContent = "Starting the chat with a representative...";
                    chatBox.removeChild(yesButton);
                    chatBox.removeChild(noButton);
                });

                // Handle No button click
                noButton.addEventListener('click', function () {
                    botMsgDiv.textContent = "Okay, feel free to ask me anything else!";
                    chatBox.removeChild(yesButton);
                    chatBox.removeChild(noButton);
                });

                chatBox.scrollTop = chatBox.scrollHeight;
            } else {
                botMsgDiv.textContent = bestResponse; // Show the best response found
            }

            chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
        }, 500);

        userInput.value = ''; // Clear input field after sending message
    }
}

function startCrispChat() {
    // Close or hide the bot chat container
    const botChatContainer = document.getElementById('chat-container');
    if (botChatContainer) {
        botChatContainer.style.display = 'none'; // Hide the bot chat container
    }

    // Check if Crisp has been initialized, and reset the session if so
    if (window.$crisp) {
        window.$crisp.push(['do', 'session:reset']);
    } else {
        // Initialize Crisp for the first time
        window.$crisp = [];
    }

    // Set the Crisp Website ID
    window.CRISP_WEBSITE_ID = "8f0f07ca-031f-4302-aaf0-1adf43a2856e";

    // Load the Crisp chat widget
    (function () {
        var d = document;
        var s = d.createElement("script");
        s.src = "https://client.crisp.chat/l.js";
        s.async = true;  // Set the script to load asynchronously
        d.getElementsByTagName("head")[0].appendChild(s);  // Append the script to the head
    })();

    // Optionally, open the chat window automatically
    window.$crisp.push(['do', 'chat:open']);
}
