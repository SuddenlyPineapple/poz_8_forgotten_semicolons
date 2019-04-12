<template>
    <div>
        <v-container>
            <v-layout row>
                 <v-flex lg4 offset-lg4 md6 xs12>
                     <h1 class="mb-3 green--text text-xs-center">Text</h1>
                </v-flex>
            </v-layout>
        </v-container>
    </div>
</template>

<script>
import {Vue, Component, Prop} from 'vue-property-decorator';
@Component()
export default class HomePage extends Vue {

}

</script>

<style scoped lang="sass">

</style>