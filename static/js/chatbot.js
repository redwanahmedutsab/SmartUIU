const responses = {
    "hello": "Hello! This is the SmartUIU Chatbot. How can I assist you?",
    "i am good": "Good to here that. How can I assist you?",
    "how are you or how are you doing": "I'm doing well. How about you?",
    "can you help me": "Of course! What do you need assistance with?",
    "how can i sign up": "To sign up, click on the 'Sign Up' button on the homepage. Fill in all the required information accurately and then click the 'Sign Up' button.",
    "how can i create an account": "To create an account, click on the 'Sign Up' button on the homepage. Fill in all the required information accurately and then click the 'Sign Up' button.",
    "how can i search for job on this website": "Once you're logged in, you can explore all available job listings on the homepage.",
    "what types of jobs are available here": "We offer a wide range of job opportunities, including roles in engineering, business, and education, among others.",
    "can you help me find a job": "Certainly! Feel free to search for jobs related to UIU or any specific field you're interested in.",
    "how do i create a profile and upload my resume": "After logging in, click on 'CV Update' under the menu at the top right. From there, you can upload your resume.",
    "how can i create my cv": "After logging in, click on 'CV Update' under the menu at the top right. From there, you can upload your resume.",
    "what are the latest job postings": "I don't have access to real-time data, so I recommend checking the homepage for the most recent job postings.",
    "what are the latest jobs available": "I don't have access to real-time data, so I recommend checking the homepage for the most recent job postings.",
    "tell me about the application process for a job I'm interested in": "The application process varies by company and job. You usually need to submit your resume and cover letter through the provided application platform.",
    "i want a help or i want some help": "tell me how can i help you?",
    "what qualifications do i need to get a job": "To determine the qualifications for a specific job position, please refer to the job description provided by the employer.",
    "what are the skills that i need to learn to get a job": "To determine the qualifications for a specific job position, please refer to the job description provided by the employer.",
    "how can i find thesis member or how can i search thesis member profile": "To find or search a thesis member you will have to click on find thesis member option on the navigation bar.",
    "how can i edit my profile information": "You can edit your profile information by clicking on 'Edit Profile' under the menu at the top right.",
    "can i set up job alerts for specific keywords or locations": "Yes, you can usually set up job alerts to receive notifications about new job listings that match your preferences.",
    "do you offer any career advice or resume tips": "We don't provide specific advice here, but I recommend checking our blog or resources section for career advice and resume tips.",
    "how can i contact the employer after applying for a job": "Usually, you can find contact information for the employer in the job posting. You can reach out via email or the provided contact details.",
    "what is the status of my job applications": "You can usually check the status of your job applications in the 'Applications' section of your profile.",
    "can you recommend some resources for interview preparation": "Check our Resources or Blog sections for articles on interview preparation tips and techniques.",
    "how do i reset my password if i forget it": "You can usually find a 'Forgot Password' link on the sign-in page. Follow the instructions to reset your password.",
    "what companies are currently hiring remote workers": "To find companies hiring remote workers, you can use the search filters to specify 'Remote' in the location or look for job descriptions mentioning remote work.",
    "can i save job listings to revisit later": "Yes, many platforms allow you to save job listings by clicking on a 'Save' or 'Bookmark' option. You can access your saved jobs in your profile.",
    "what benefits and perks are offered by [specific company]": "To learn about benefits and perks offered by a specific company, check their job postings or company profile.",
    "how do i apply for an internship or entry-level position": "You can apply for internships or entry-level positions by searching for relevant job listings and following the application process outlined in the posting.",
    "tell me more about the salary range for [specific job title]": "Salary ranges can vary widely based on the role, location, and company. I recommend researching industry standards and checking job postings for salary information.",
    "how do i create a new account on this website": "To create a new account, click on the 'Sign Up' button and provide the required information.",
    "can i sign up using my social media accounts": "Yes, many platforms offer the option to sign up using your social media accounts for convenience.",
    "what should i do if i forgot my password": "If you forgot your password, click on the 'Forgot Password' link on the sign-in page and follow the instructions to reset it.",
    "is there an option for two-factor authentication during sign-in": "Two-factor authentication is an added security feature offered by some platforms. You can usually enable it in your account settings.",
    "how can i change my account password": "You can usually change your account password in the 'Account Settings' section of your profile.",
    "can i edit my profile information after signing up": "Yes, you can edit your profile information after signing up by accessing the 'Edit Profile' section in your account settings.",
    "what's the difference between signing in and signing up": "Signing in is for users who already have an account. Signing up is for creating a new account if you don't have one.",
    "how can i post a job vacancy on your website": "To post a job vacancy, log in to your account and find the 'Post a Job' option. Fill in the required details and submit the job listing.",
    "what information is required when posting a job": "When posting a job, you'll typically need to provide details such as job title, description, requirements, location, and application instructions.",
    "how long will my job posting be visible on the site": "Job posting durations can vary. You can usually select the duration when posting the job or refer to the platform's guidelines.",
    "can i edit or delete a job posting after it's been published": "Yes, you can often edit or delete a job posting from your account's 'Job Listings' section.",
    "is there a fee for posting job vacancies": "Fees for posting job vacancies can vary. Check the platform's pricing information or guidelines.",
    "how can i search for jobs in a specific industry": "You can search for jobs in a specific industry by using relevant keywords in the search bar or by applying industry filters.",
    "is there a way to filter job listings by location": "Yes, you can usually filter job listings by location to find opportunities in specific areas.",
    "can i search for remote job opportunities": "Yes, you can search for remote job opportunities by using the remote work filter in the search options.",
    "what advanced search options are available for job seekers": "Advanced search options may include filters for job type, salary range, experience level, and more.",
    "how do i save job listings to review later": "You can usually save job listings by clicking on a 'Save' or 'Bookmark' option in the listing. Access your saved jobs in your profile.",
    "can i set up email alerts for new job listings": "Yes, many platforms offer the option to set up email alerts for new job listings matching your preferences.",
    "how can i find thesis topics related to my field of study": "To find thesis topics, you can search online research databases, academic journals, and consult with your professors or advisors.",
    "are there any resources for writing research papers or theses": "You can find resources for writing research papers and theses in libraries, academic websites, and online writing guides.",
    "can i contact researchers or students working on similar topics": "You can often contact researchers or students by reaching out via academic platforms, conferences, or networking events.",
    "how do i submit my thesis for consideration on this platform": "Check the platform's guidelines for thesis submission. You may need to provide details about your thesis and upload relevant documents.",
    "is there a way to collaborate on research projects": "Collaboration on research projects can occur through academic networks, conferences, and reaching out to researchers directly.",
    "how can i connect with other professionals or researchers": "You can connect with professionals and researchers through networking events, conferences, and academic platforms.",
    "is there a directory of members on this platform": "Some platforms have a directory of members that you can access to connect with professionals in your field.",
    "can i send private messages to other users for networking": "Yes, many platforms offer the option to send private messages to connect and network with other users.",
    "how do i join groups or communities related to my field": "You can often join groups or communities on the platform by searching for relevant groups and requesting to join.",
    "are there any upcoming job events or are there any new job events": "Check the platform's events section for information about upcoming networking events and conferences.",
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

        // Initialize the bot's response as "I don't understand" by default
        let botMessage = "I'm sorry, I don't understand.";

        // Find the query with the longest common subsequence with the user's message
        let maxLCSLength = 0;
        for (const query in responses) {
            const lcs = longestCommonSubsequence(userMessage.toLowerCase(), query.toLowerCase());
            if (lcs.length > maxLCSLength) {
                maxLCSLength = lcs.length;
                botMessage = responses[query];
            }
        }

        // Simulate bot response
        setTimeout(function () {
            const botMsgDiv = document.createElement('div');
            botMsgDiv.classList.add('bot-msg');
            botMsgDiv.textContent = botMessage;
            chatBox.appendChild(botMsgDiv);

            // Scroll chat box to bottom
            chatBox.scrollTop = chatBox.scrollHeight;
        }, 500);

        userInput.value = '';
    }
}