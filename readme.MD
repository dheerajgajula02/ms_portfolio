## My portfolio inital commit 

- Avilable at [portfolio.dheerajg.me](https://portfolio.dheerajg.me)

- Steps to host on a VM

    - You need a VM on one of the cloud providers or a public IP
    - A domain name to route 
    - make your server a service in the VM with public IP refer the following template

    - ```[Unit]
        Description=Streamlit Application
        After=network.target

        [Service]
        ExecStart=/home/dheerajgajula_ma/portfolio/venv/bin/streamlit run /home/dheerajgajula_ma/portfolio/main.py --server.headless true --server.port 8501
        WorkingDirectory=/home/dheerajgajula_ma/portfolio
        User=dheerajgajula_ma
        Restart=always

        [Install]
        WantedBy=multi-user.target 
        ```

    - write the basic configuration for the nginx, refer the following code snippet     

    - ```
        server {
        server_name portfolio.dheerajg.me;

        location / {
            proxy_pass http://localhost:8501/;  # Ensure this points to your Streamlit app
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;  # Handle WebSocket upgrade
            proxy_set_header Connection "upgrade";    # Handle WebSocket connection
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            }
        }
        ```
        

    - Link the same file in sites-avilable folder and sites-enabled folder :
    
        -  ``` sudo ln -s /etc/nginx/sites-available/portfolio.dheerajg.me /etc/nginx/sites-enabled/ ```

    - Now use certbot to get free SSL certificate

        - installing : ``` apt install certbot python3-certbot-nginx ```
        - Issuing : ```certbot --nginx -d portfolio.dheerajg.me```
        - renewal : ``` certbot renew --dry-run  ```

    - The nginx configuration will change and will look something like this 

    - ```
        server {
        server_name portfolio.dheerajg.me;
        location / {
            proxy_pass http://localhost:8501/;  # Ensure this points to your Streamlit app
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;  # Handle WebSocket upgrade
            proxy_set_header Connection "upgrade";    # Handle WebSocket connection
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        listen 443 ssl; # managed by Certbot
        ssl_certificate /etc/letsencrypt/live/portfolio.dheerajg.me/fullchain.pem; # managed by Certbot
        ssl_certificate_key /etc/letsencrypt/live/portfolio.dheerajg.me/privkey.pem; # managed by Certbot
        include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
        }
        server {
            if ($host = portfolio.dheerajg.me) {
                return 301 https://$host$request_uri;
            } # managed by Certbot
            listen 80;
            server_name portfolio.dheerajg.me;
            return 404; # managed by Certbot
        }
        ```