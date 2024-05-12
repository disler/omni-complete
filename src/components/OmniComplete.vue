<template>
  <div class="omnicomplete-w">
    <input
      class="omni-input omni-shared"
      type="text"
      @keydown="keyPressed"
      v-model="inputValue"
      @keydown.tab.prevent="tabPressed"
      @keydown.enter.prevent="enterPressed"
      :placeholder="placeholder"
    />
    <input
      class="omni-completion omni-shared"
      v-model="completionsDisplay"
      :disabled="true"
      @click="focusInput"
    />
    <div class="gradient-div"></div>
  </div>
</template>

<script lang="ts" setup>
import { computed, nextTick, ref, toRefs } from "vue";
import { useDebounceFn } from "@vueuse/core";

interface Props {
  completions?: string[];
  topic: string;
}

const props = defineProps<Props>();
const { completions, topic } = toRefs(props);

const emit = defineEmits([
  "get-autocomplete",
  "use-autocomplete",
  "clear-completions",
  "enter-pressed",
]);

const inputValue = ref("");
const inputRef = ref<HTMLInputElement | null>(null);

const didAutocomplete = ref(false);

const completion = computed(() => {
  return completionsDisplay.value || "";
});

const placeholder = computed(() => {
  return `Ask me anything about ${topic.value}`;
});

const completionsDisplay = computed<string>(() => {
  if (!completions.value) {
    return "";
  }
  const firstCompletion = completions.value[0];
  if (!firstCompletion) {
    return "";
  }
  return `${inputValue.value.trim()} ${firstCompletion}`;
});

function tabPressed() {
  const inputPreCompletion = inputValue.value;
  const completionSuffix = completions.value?.[0];

  inputValue.value = completion.value;
  didAutocomplete.value = true;

  emit("use-autocomplete", inputPreCompletion, completionSuffix);

  nextTick(() => {
    inputRef.value?.scrollTo(inputRef.value.scrollWidth, 0);
  });
}

function enterPressed() {
  emit("enter-pressed", inputValue.value);
  inputValue.value = "";
  didAutocomplete.value = false;
}

const keyPressedDebounce = useDebounceFn(function (_event: KeyboardEvent) {
  if (didAutocomplete.value) {
    return;
  }
  if (inputValue.value.length === 0) {
    didAutocomplete.value = false;
    return;
  }
  if (inputValue.value.split(" ").length < 3) {
    return;
  }
  emit("get-autocomplete", inputValue.value);
}, 500);

function keyPressed(event: KeyboardEvent) {
  emit("clear-completions");
  keyPressedDebounce(event);
  if (inputValue.value === "") {
    didAutocomplete.value = false;
  }
}

function focusInput() {
  inputRef.value?.focus();
}
</script>

<style scoped>
.omnicomplete-w {
  position: relative;
  width: 100%;
  height: 100%;
}

.omni-input {
  width: 100%;
  height: 100%;
  position: relative;
  z-index: 1;
  background: rgb(8, 8, 8);
}

.omni-completion {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  border: 1px solid transparent;
  background: transparent;
  color: #fffd8280;
  z-index: 11;
  pointer-events: none;
  text-shadow: 0 0 10px yellow;
}

.omni-shared {
  border-radius: 10px;
  padding: 5px 15px;
  box-shadow: 0 0px 13px rgba(21, 59, 129, 0.822),
    0 0px 13px rgba(149, 19, 19, 0.769);
  border: none;
  outline: none;
  transition: box-shadow 0.3s ease-in-out, background 0.3s ease-in-out;
  font-size: 20px;
}

.omni-shared:focus {
  box-shadow: 0 0px 44px rgba(20, 77, 184, 0.98),
    0 0px 44px rgba(186, 15, 15, 0.95);
  background: rgb(0, 0, 0);
}

.gradient-div {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, #ff0000, #00ff00, #0000ff);
  background-size: 600% 600%;
  animation: gradientAnimation 10s ease infinite;
  border-radius: 50%;
  filter: blur(50px);
  z-index: -1;
}

@keyframes gradientAnimation {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
</style>
