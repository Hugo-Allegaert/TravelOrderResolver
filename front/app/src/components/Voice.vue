<template>
    <div class="input-voice-container">
        <div class="voice-text">
          <p v-if="error" style="color: gray">{{error}}</p>
          <div v-else>
            <span>{{sentence}}</span>
            <span>{{runtimeTranscription}}</span>
          </div>
        </div>
        <div>
            <span @click.stop="toggle ? endSpeechRecognition() : startSpeechRecognition()">
                <i class="icon fas fa-microphone" :class="{'hidden': toggle}"></i>
                <i class="icon disable fas fa-microphone-slash" :class="{'hidden': !toggle}"></i>
            </span>
        </div>
      </div>
</template>

<script>
let SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
let recognition = SpeechRecognition? new SpeechRecognition() : false

export default {
    name: 'Voice',
    props: {
    lang: {
      type: String,
      default: 'fr-FR'
      }
    },
    model: {
      prop: 'text',
      event: 'update:text'
    },
  data () {
    return {
      error: false,
      toggle: false,
      runtimeTranscription: '',
      sentence: ''
    }
  },
  methods: {
    checkCompatibility () {
      if (!recognition) {
        this.error = "La reconnaissance vocale n'est pas disponible sur ce navigateur. Veuillez utiliser Chrome ou Firefox"
      }
    },
    endSpeechRecognition () {
      recognition.stop()
      this.toggle = false
      this.$emit('speechend', {
        sentence: this.sentence,
      })
    },
    startSpeechRecognition () {
      if (!recognition) {
        this.error = "La reconnaissance vocale n'est pas disponible sur ce navigateur. Veuillez utiliser Chrome ou Firefox"
        return false
      }
      if (this.toggle == false) {
        this.toggle = true
        this.sentence = ''
        recognition.lang = this.lang
        recognition.interimResults = true

        recognition.addEventListener('result', event => {
            const text = Array.from(event.results).map(result => result[0]).map(result => result.transcript).join('')
            this.runtimeTranscription = text
        })

        recognition.addEventListener('end', () => {
            if (this.runtimeTranscription !== '') {
                this.sentence = this.capitalizeFirstLetter(this.runtimeTranscription)
                this.$emit('update:text', `${this.sentence}.`)
            }
            this.runtimeTranscription = ''
            recognition.stop()
            this.toggle = false
        })
        recognition.start()
      }
    },
    capitalizeFirstLetter (string) {
      return string.charAt(0).toUpperCase() + string.slice(1)
    }
  },
  mounted () {
    this.checkCompatibility()
  }
}
</script>

<style scoped>
.input-voice-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    background-color: white;
    color: #000;
    border-radius: 2px;
    text-decoration: none;
    box-shadow: 0 2px 1px -1px rgb(0 0 0 / 20%), 0 1px 1px 0 rgb(0 0 0 / 14%), 0 1px 3px 0 rgb(0 0 0 / 12%);
}

.voice-text {
    max-width: 85%;
}

.icon {
    width: 20px;
    height: 20px;
    padding: 6px;
    background-color: #a2a2a2;
    color: white;
    border-radius: 100%;
}

.icon.disable {
    background: rgb(211, 58, 67);
    transform: scale(1);
    animation: pulse 2s infinite;
}

@keyframes pulse {
	0% {
		transform: scale(0.95);
		box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.7);
	}

	70% {
		transform: scale(1);
		box-shadow: 0 0 0 10px rgba(0, 0, 0, 0);
	}

	100% {
		transform: scale(0.95);
		box-shadow: 0 0 0 0 rgba(0, 0, 0, 0);
	}
}

.hidden {
    display: none;
}
</style>