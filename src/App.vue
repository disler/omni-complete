<template>
  <div class="app">
    <h1>omniComplete</h1>
    <div class="autocomplete-wrapper">
      <OmniComplete
        :completions="completions"
        :topic="topic"
        @use-autocomplete="onUseAutocomplete"
        @get-autocomplete="onGetAutocomplete"
        @clear-completions="onClearCompletions"
        @enter-pressed="onEnterPressed"
      />
    </div>
    <div class="stars">
      <div
        class="star"
        v-for="i in 1000"
        :key="i"
        :style="starPositions[i]"
      ></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import OmniComplete from "./components/OmniComplete.vue";

const completions = ref<string[]>([]);
const starPositions = ref(
  Array.from({ length: 1000 }, () => ({
    top: `${Math.random() * 100}%`,
    left: `${Math.random() * 100}%`,
    opacity: `${Math.random()}`,
  }))
);
const topic = ref("Vue.js & UnoCSS");

async function onUseAutocomplete(input: string, completion: string) {
  console.log("onUseAutocomplete", input, completion);
  fetch("http://127.0.0.1:5000/use-autocomplete", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ input: input, completion: completion }),
  });
}

async function onGetAutocomplete(completion: string) {
  console.log("onGetAutocomplete", completion);

  const response = await fetch("http://127.0.0.1:5000/get-autocomplete", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ input: completion }),
  });

  const jsonData = await response.json();
  const data = JSON.parse(jsonData);

  console.log("Autocomplete response:", data);
  console.log("Autocomplete response.completions:", data.completions);

  completions.value = data.completions || [];
  console.log(`completions.value`, completions.value);
}

function onEnterPressed(value: string) {
  console.log(`Do something with your autocompleted value`, value);
}

function onClearCompletions() {
  completions.value = [];
}
</script>

<style scoped>
.app {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 90vh;
}
.stars {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  overflow: hidden;
}

.star {
  position: absolute;
  width: 2px;
  height: 2px;
  background-color: white;
  border-radius: 50%;
  opacity: 0;
  animation: twinkle 5s infinite;
}

@keyframes twinkle {
  0% {
    opacity: 0;
  }
  50% {
    opacity: 0.4;
  }
  100% {
    opacity: 0;
  }
}

.autocomplete-wrapper {
  width: 500px;
  height: 65px;
}
</style>
