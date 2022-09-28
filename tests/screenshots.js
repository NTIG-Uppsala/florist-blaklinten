const puppeteer = require('puppeteer');
const fs = require('fs');

async function runTest() {

    if (!fs.existsSync("screenshots")) {
        fs.mkdirSync("screenshots");
    }

    const browser = await puppeteer.launch({
        headless: true,
        timeout: 150 * 1000, // 2.5 min timeout per task
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const url_list = [
        'index.html',
        'index-ua.html',
    ];

    const resolutions = [
        {width: 1920, height: 1080 },
        {width: 2560, height: 1440 },
        {width: 1366, height: 768  },
        {width: 360,  height: 640  },  
        {width: 820,  height: 1180 }, 
        {width: 414,  height: 896  }, 
        {width: 1536, height: 864  },  
    ];


    // Loop through every page
    for (let i = 0; i < url_list.length; i++) {
        let page = await browser.newPage();

        const url = `http://localhost:3000/${url_list[i]}`;

        await page.goto(url, {
            waitUntil: 'networkidle2'
        });

        // Loop through every resolution
        for (let index = 0; index < resolutions.length; index++) {
            const current_resolution = resolutions[index];
    
            // set viewport width and height
            await page.setViewport({ 
                width: current_resolution.width, 
                height: current_resolution.height 
            });
        
            await page.screenshot({ path: `screenshots/${url_list[i]}_${current_resolution.width}x${current_resolution.height }.png`, fullPage: true });
        }

    }

    browser.close(); 
    
}

runTest();