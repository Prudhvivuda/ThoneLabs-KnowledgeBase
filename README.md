**Lab 100 Knowledge Base**

LAB100_KB_AUTH_KEY=INGH
LAB100_KB_AUTH_SECRET=isgreat

**How to install**

    cd desired/path/to/lab100kb

    git clone https://yourusername@bitbucket.org/MaxTomlinson/lab100kb.git

    virtualenv env ( python -m virtualenv env)

    source env/bin/activate (  source env/Scripts/activate)

    pip install -r requirements.txt

    #to testrun server with basic testing flask server you can run:

    python patient_normalization_app.py

    #to run an easy gunicorn server, run (current incarnation):

    #The server is running on port 8000 - this specific port is necessary for default nginx.

    nohup gunicorn --timeout 120 patient_normalization_app:app --workers=4 --threads=2 -b localhost:8000 > kb_out.out &



**Links:**

[KB Final Write Up](https://docs.google.com/document/d/1x2ZovqvZ1ZUdpLhMf_LABccc1yG8sBuR3i0WV-G3fRg/edit?usp=sharing)

[Description of each file and API](https://docs.google.com/document/d/1EzeDIWRDnbKNb_h_sxjA1bmemjS745MnbjPXBlNWg6Y/edit?usp=sharing)

[Summary of metrics](https://docs.google.com/document/d/1ZndIecIRAZSI_Z-jkgZbMoPK6j8oRNU0SrhWscWSRzA/edit?usp=sharing)

[Lab100kb Normalization Explanation](https://docs.google.com/document/d/1R-YbjQ9vpBTzKHhUzlkf-CWohusP8yCCurKS441mPug/edit?usp=sharing)
