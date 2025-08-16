<div>
<h1>Technical agreements</h1>
<p>1. Not all vacancies are fully compatible</p>
<p>2. The script is intentionally slowed down when parsing data to protect against DDoS attacks</p>
<p>3. There are only 4 positions on the abscissa: 
 * 1 year - no work experience;
 * 3 - 1 - 3 years of work experience;
 * 6 - 3 - 6 years of work experience;
 * 7 - more than 6 years of work experience</p>
<p>4. Salaries are listed in the median order for greater accuracy</p>
<p>5. For convenience, a file with the 'settings.json' (aka 'settingsbase.json') file base has been created
</p>
</div>

<div>
<h1>How to use?</h1>
<p>Create a 'settings.json' file in current directory that contains the input parameters. Fill in the parameters with the appropriate data. The required files in the project's directory are listed below:</p>
<img src=".\READMEdata\mustHaveFiles.png">
<p>The parameter names and types are listed below:</p>
<img src=".\READMEdata\settingTypes.png">
<p>Next, run the 'main.py' file as you prefer:</p>
<img src=".\READMEdata\howToLaunch.png">
<p>If you have done everything correctly and have not forgotten to specify the parameters for a particular job, the script should display something similar:</p>
<img src=".\READMEdata\inProcessing.png">
</div>

<div>
<h1>Example</h1>
<p>A 'settings.json' file has been created in the same directory as the script. The contents of the file are:</p>
<img src=".\READMEdata\settingsExample.png">
<p>Running the script in powershell:</p>
<img src=".\READMEdata\howToLaunch.png">
<p>We wait for the script to execute and get the following output in the console:</p>
<img src=".\READMEdata\outputInConsoleExample.png">
<p>A new window with an information chart showing the specified vacancies is also displayed:</p>
<img src=".\READMEdata\resultGraphicExample.png">
<p>This graph is based on 'matplotlib', so you can work with it in the same way</p>
<p>Thanks for read!</p>
</div>