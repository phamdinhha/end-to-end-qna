<template>
  <!-- eslint-disable max-len -->
  <div class='bertOnlyUI'>
    <h1 class='instagram'>Simple Question Answering System</h1>
    <h2>with bert only</h2>
    <p>
      <center>
      by HaPhamD
      </center>
    </p>
    <link
      rel="stylesheet"
      href="https://use.fontawesome.com/releases/v5.8.2/css/all.css"
      integrity="sha384-oS3vJWv+0UjzBfQzYUhtDYW+Pj2yciDJxpsK1OYPAYjqT085Qq/1cq5FLXAZQ7Ay"
      crossorigin="anonymous"
    >
    <div class='input m-4'>
      <b-form @submit="onSubmit">
        <label>Question</label>
        <b-input-group>
          <b-form-input v-model="query" placeholder="Put your question here"></b-form-input>
          <b-input-group-append>
            <b-button class="gradient-fill background hover" @click="onSubmit">
              <b-spinner v-if="status == 'loading'" small :variant="'white'" label="Spinner"></b-spinner>
              <i v-else class="fa fa-search"></i>
            </b-button>
          </b-input-group-append>
        </b-input-group>
        <label>Context</label>
        <b-input-group>
          <textarea v-model="paragraph" placeholder='Put your context here' rows="5" style="width: 100%;"></textarea>
        </b-input-group>
      </b-form>
      <br>

      <div v-if="this.status == 'done' && this.query != ''">
        <div class='mb-4'>
          <span class='gradient-fill'>Answer</span>
          <br>
          <span>{{ answer }}</span>
        </div>
        <div class='mb-4'>
          <span class='gradient-fill'>Passage Context</span>
          <br>
          <span>{{ paragraph }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'bertOnlyUI',
  props: {
    api_endpoint: {
      type: String,
      default: 'http://localhost:5000/bertonly',
    },
  },
  data() {
    return {
      query: '',
      status: 'started',
      answer: '',
      paragraph: '',
    };
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      this.status = 'loading';
      axios
        .get(this.apiEndpoint, { params: { query: this.query, paragraph: this.paragraph } })
        .then((response) => {
          this.answer = response.data.answer;
          this.paragraph = response.data.paragraph;
          this.status = 'done';
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>

<style scoped>
.hpqaUI {
  text-align: left;
  font-family: Inter, Inter UI, Inter-UI, SF Pro Display, SF UI Text,
    Helvetica Neue, Helvetica, Arial, sans-serif;
  font-weight: 400;
  letter-spacing: +0.37px;
  color: rgb(175, 175, 175);
}

.form-control:focus {
  border-color: #ae41a7 !important;
  box-shadow: 0 0 5px #ae41a7 !important;
}

.instagram{
  text-align: center;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-weight: 800;
  letter-spacing: +0.37px;
  color: rgb(255, 255, 255);
  background: #f09433;
  background: -moz-linear-gradient(
    45deg,
    #f09433 0%,
    #e6683c 25%,
    #dc2743 50%,
    #cc2366 75%,
    #bc1888 100%
  );
  background: -webkit-linear-gradient(
    45deg,
    #f09433 0%,
    #e6683c 25%,
    #dc2743 50%,
    #cc2366 75%,
    #806878 100%
  );
  background: linear-gradient(45deg,
    #f09433 0%,
    #e6683c 25%,
    #dc2743 50%,
    #cc2366 75%,
    #bc1888 100%
  );
  filter: progid:DXImageTransform.Microsoft.gradient( startColorstr=#f09433,
    endColorstr=#bc1888,
    GradientType=1
  );
}

.header {
  text-align: center;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-weight: 800;
  letter-spacing: +0.37px;
  color: rgb(255, 255, 255);
  background-image: linear-gradient(
    -225deg,
    #a445b2 0%,
    #d41872 52%,
    #ff0066 100%
  );
}

.gradient-fill {
  background-image: linear-gradient(
    -225deg,
    #a445b2 0%,
    #d41872 52%,
    #ff0066 100%
  );
}

.gradient-fill.background {
  background-size: 250% auto;
  border: medium none currentcolor;
  border-image: none 100% 1 0 stretch;
  transition-delay: 0s, 0s, 0s, 0s, 0s, 0s;
  transition-duration: 0.5s, 0.2s, 0.2s, 0.2s, 0.2s, 0.2s;
  transition-property: background-position, transform, box-shadow, border,
    transform, box-shadow;
  transition-timing-function: ease-out, ease, ease, ease, ease, ease;
  color: white;
  font-weight: bold;
  border-radius: 3px;
}

span.gradient-fill {
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 20px;
  font-weight: 700;
  line-height: 2.5;
}

</style>
