
let timers = {}

document.addEventListener("DOMContentLoaded", function() {
    const times = document.querySelectorAll('.times')
    times.forEach(time =>{

       if (time.textContent !== undefined && time.textContent !== "") {
            timers[time.id] = new Timer(time)
            timers[time.id].startTime()
        }
    })

})


class Timer{
    constructor(startTimeElement) {
        this.startTimeElement = startTimeElement
        this.hour = 0;
        this.minute = 0;
        this.second = 0;
        this.count = 0;
        this.timer;
        this.prepareTime();
    }

    prepareTime(){
        const start_time = Date.parse(this.startTimeElement.textContent)
        const now = new Date().getTime()

        const h = Math.round((now / (1000*60*60) - (start_time / (1000*60*60))) % 24)
        const m = Math.round((now / (1000*60) - (start_time / (1000*60))) % 60)
        const s = Math.round((now / (1000) - (start_time / (1000))) % 60)
        console.log(h)
        console.log(m)
        console.log(s)

        this.hour = h;
        this.minute = m;
        this.second = s;
        this.count = 0;
    }

    startTime() {
        this.count++;

        if (this.count === 100) {
            this.second++;
            this.count = 0;
        }

        if (this.second === 60) {
            this.minute++;
            this.second = 0;
        }

        if (this.minute === 60) {
            this.hour++;
            this.minute = 0;
            this.second = 0;
        }

        let hrString = this.hour;
        let minString = this.minute;
        let secString = this.second;
        let countString = this.count;

        if (this.hour < 10) {
            hrString = "0" + hrString;
        }

        if (this.minute < 10) {
            minString = "0" + minString;
        }

        if (this.second < 10) {
            secString = "0" + secString;
        }

        if (this.count < 10) {
            countString = "0" + countString;
        }

        document.getElementById(`hr-${this.startTimeElement.id}`).innerHTML = hrString;
        document.getElementById(`min-${this.startTimeElement.id}`).innerHTML = minString;
        document.getElementById(`sec-${this.startTimeElement.id}`).innerHTML = secString;
        document.getElementById(`count-${this.startTimeElement.id}`).innerHTML = countString;
        setTimeout(this.startTime.bind(this), 10);
    }
}