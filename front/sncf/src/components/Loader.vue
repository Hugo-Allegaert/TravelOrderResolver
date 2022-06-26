<template>
<div class="fa-3x">
    <div class="loader-box">
        <span class="loader-text">Recherche en cours</span>
    
        <svg version="1.1" id="L5" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 100 100" enable-background="new 0 0 0 0" xml:space="preserve">
            <circle fill="black" stroke="none" cx="6" cy="50" r="6">
                <animateTransform 
                    attributeName="transform" 
                    dur="1s" 
                    type="translate" 
                    values="0 15 ; 0 -15; 0 15" 
                    repeatCount="indefinite" 
                    begin="0.1"/>
            </circle>
            <circle fill="black" stroke="none" cx="30" cy="50" r="6">
                <animateTransform 
                    attributeName="transform" 
                    dur="1s" 
                    type="translate" 
                    values="0 10 ; 0 -10; 0 10" 
                    repeatCount="indefinite" 
                    begin="0.2"/>
            </circle>
            <circle fill="black" stroke="none" cx="54" cy="50" r="6">
                <animateTransform 
                    attributeName="transform" 
                    dur="1s" 
                    type="translate" 
                    values="0 5 ; 0 -5; 0 5" 
                    repeatCount="indefinite" 
                    begin="0.3"/>
            </circle>
        </svg>
    </div>
</div>
</template>

<script>
export default {
  name: 'Loader'
}
</script>

<style scoped>

.loader-box {
    margin-top: 20%;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    background-image: url("/img/bg.png");
    color: black
}

.loader-text {
    font-weight: bold;
    margin-top: auto;
    margin-bottom: auto;
}

svg {
  width: 100px;
  height: 100px;
  margin: 20px;
  display: inline-block;
}
</style>