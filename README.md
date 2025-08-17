# x-posting

## Buat file autopost.yml 

.github/workflows/autopost.yml

file di bawah

## Link API

1. Gemini API : https://aistudio.google.com/apikey or https://console.cloud.google.com/cloud-resource-manager?pli=1&inv=1&invt=Ab2jrA
2. x.com API : https://developer.x.com/en/portal/dashboard

## Konfigurasi GitHub Secrets

1. Di repositori GitHub Anda, buka Settings > Secrets and variables > Actions.
2. Klik New repository secret untuk setiap kunci API.
3. Buat secret dengan nama-nama berikut (sesuai yang ada di file .yml dan .py):

        GEMINI_API_KEY
        X_API_KEY
        X_API_SECRET
        X_BEARER_TOKEN
        X_ACCESS_TOKEN
        X_ACCESS_TOKEN_SECRET

Salin dan tempel nilai kunci API Anda ke masing-masing secret.

4. Setelah semua langkah di atas selesai, GitHub Actions akan secara otomatis menjalankan skrip main.py pada jadwal yang telah Anda tentukan di autopost.yml.

## Themplat pengajuan API ke x.com

		Our application will leverage the X API to provide users with enhanced social media management and analytics capabilities. The primary use cases for accessing X's data and API are as follows:

		Content Publishing and Scheduling: Our service will allow users to compose, schedule, and publish posts directly to their X account. This requires write access to post on behalf of the user, who will have to explicitly grant this permission through OAuth. We will also retrieve user information, such as profile details, to ensure posts are correctly attributed.

		Social Media Monitoring and Analytics: We will access public data, including mentions, hashtags, and keywords relevant to our users' brands or topics of interest. This enables us to provide analytics on reach, engagement, and sentiment analysis. We will also retrieve data on users' own posts to report on their performance. This functionality relies on read access to public posts and user timelines.

		Customer Engagement and Support: Our platform will enable users to monitor their mentions and direct messages, allowing for timely responses to customer inquiries and feedback. This requires access to a user's mentions and direct messages, which will be granted through user authentication and authorization.

		All data accessed through the X API will be handled in strict accordance with our privacy policy and the X Developer Policy. We are committed to data minimization and will only request permissions for the data that is essential to deliver our services. User data will be securely stored and will not be shared with any third parties without explicit user consent. We will maintain transparent and easily accessible information about the data we collect and how it is used.
	

