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
    "what are the benefits of creating an account here": "By creating an account on SmartUIU, you gain access to exclusive features like the Lost & Found section, Thesis Member Finder, upcoming Home Finder, Marketplace, and personalized event recommendations. It also enables you to interact with the community and manage your own listings."
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

    return lcs;
}

const userInput = document.getElementById('user-input');
userInput.addEventListener('keyup', function (event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');

    const userMessage = userInput.value.trim();
    if (userMessage !== '') {
        const userMsgDiv = document.createElement('div');
        userMsgDiv.classList.add('user-msg');
        userMsgDiv.textContent = userMessage;
        chatBox.appendChild(userMsgDiv);

        let botMessage = "I'm sorry, I don't understand.";

        let maxLCSLength = 0;
        for (const query in responses) {
            const lcs = longestCommonSubsequence(userMessage.toLowerCase(), query.toLowerCase());
            if (lcs.length > maxLCSLength) {
                maxLCSLength = lcs.length;
                botMessage = responses[query];
            }
        }

        setTimeout(function () {
            const botMsgDiv = document.createElement('div');
            botMsgDiv.classList.add('bot-msg');
            botMsgDiv.textContent = botMessage;
            chatBox.appendChild(botMsgDiv);

            chatBox.scrollTop = chatBox.scrollHeight;
        }, 500);

        userInput.value = '';
    }
}