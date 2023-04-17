import { Field, Formik, Form } from "formik";
import * as Yup from "yup"
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  FormErrorMessage,
  FormHelperText,
  Input,
  SimpleGrid
} from "@chakra-ui/react"

import axios from "axios";

const TransactionForm = (props) => {
  const initialValues = {
    street: "",
    floor: 0,
    district: 1,
    propertyType: "",
    area: 0,
    price: 0,
    transactionDate: new Date(),
    tenure: 0,
    resale: ""
  }

  const onSubmit = values => {



    // let options = {
    //   headers: {
    //     'Content-Type': 'multipart/form-data'
    //   },
    //   method: 'POST'
    // };

    // options.body = new FormData();
    // for (let key in values) {
    //   console.log(key, values[key])
    //   options.body.append(key, values[key]);
    //   console.log("body " + options.body)
    // }
    // console.log("options " + options)
    axios.post('http://localhost:5000/addpropertytransaction', {
      values
      // street: values.street
    })
      .then((response) => {
        console.log(response);
      }, (error) => {
        console.log(error);
      });

    // fetch('http://localhost:5000/addpropertytransaction', options)
    //   .then(response => console.log(response))
    //   .catch(error => console.error(error))
  }

  const validationSchema = Yup.object({
    street: Yup.string().required("Street is required!"),
    floor: Yup.number()
      .required("Floor level is required!"),
    district: Yup.number()
      .min(1, "District must be larger than 0")
      .max(28, "Singapore only has 28 districts")
      .required("District is required!"),
    propertyType: Yup.string().required("Property type is required!"),
    area: Yup.number()
      .positive("Area must be positive")
      .required("Area is required!"),
    price: Yup.number()
      .positive("Price must be higher than $0.00")
      .required("Price is required!"),
    transactionDate: Yup.date()
      .max(new Date(), "Property has to be sold"),
    tenure: Yup.number()
      .positive("Property must have tenure left")
      .required("Tenure is required!"),
    resale: Yup.string()
      .lowercase().matches("resale" || "private", "Has to be either resale or private")
      .required("Resale/ Private is required!"),
  })

  return (
    <Box pt={{ base: "130px", md: "80px", xl: "80px" }}>
      <SimpleGrid
        columns={{ base: 1, md: 2, lg: 3, "2xl": 6 }}
        gap="20px"
        mb="20px">
        <Formik
          initialValues={initialValues}
          validationSchema={validationSchema}
          onSubmit={onSubmit}
          // method="POST"
        // onSubmit={(values, actions) => {
        // setTimeout(() => {
        //   alert(JSON.stringify(values, null, 2))
        //   actions.setSubmitting(false)
        // }, 1000)

        // let options = {
        //   headers: {
        //     'Content-Type': 'multipart/form-data'
        //   },
        //   method: 'POST'
        // };

        // options.body = new FormData();
        // for (let key in values) {
        //   options.body.append(key, values[key]);
        // }

        // fetch('http://localhost:5000/addpropertytransaction', options)
        //   .then(response => console.log(response))
        //   .catch(error => console.error(error))
        // }}
        >
          {(props) => (
            <Form action='http://localhost:5000/addpropertytransaction' method="post">
              <Field name="street">
                {({ field, form }) => (
                  <FormControl isInvalid={form.errors.street && form.touched.street}>
                    <FormLabel htmlFor="street">Street</FormLabel>
                    <Input
                      {...field}
                      id="street"
                      placeholder="Street Name"
                      borderRadius="16px"
                    />
                    <FormErrorMessage>{form.errors.street}</FormErrorMessage>
                  </FormControl>
                )}
              </Field>

              <Field name="floor">
                {({ field, form }) => (
                  <FormControl isInvalid={form.errors.floor && form.touched.floor}>
                    <FormLabel htmlFor="floor">Floor Level</FormLabel>
                    <Input
                      {...field}
                      id="floor"
                      type="number"
                      borderRadius="16px"
                    />
                    <FormErrorMessage>{form.errors.floor}</FormErrorMessage>
                  </FormControl>
                )}
              </Field>

              <Field name="district">
                {({ field, form }) => (
                  <FormControl isInvalid={form.errors.district && form.touched.district}>
                    <FormLabel htmlFor="district">District Number</FormLabel>
                    <Input
                      {...field}
                      id="district"
                      type="number"
                      borderRadius="16px"
                    />
                    <FormErrorMessage>{form.errors.district}</FormErrorMessage>
                  </FormControl>
                )}
              </Field>

              <Field name="propertyType">
                {({ field, form }) => (
                  <FormControl isInvalid={form.errors.propertyType && form.touched.propertyType}>
                    <FormLabel htmlFor="propertyType">Property Type</FormLabel>
                    <Input
                      {...field}
                      id="Property Type"
                      placeholder="Property Type"
                      borderRadius="16px"
                    />
                    <FormErrorMessage>{form.errors.propertyType}</FormErrorMessage>
                  </FormControl>
                )}
              </Field>

              <Field name="area">
                {({ field, form }) => (
                  <FormControl isInvalid={form.errors.area && form.touched.area}>
                    <FormLabel htmlFor="area">Area (in square metre)</FormLabel>
                    <Input
                      {...field}
                      id="area"
                      type="number"
                      borderRadius="16px"
                    />
                    <FormErrorMessage>{form.errors.area}</FormErrorMessage>
                  </FormControl>
                )}
              </Field>

              <Field name="price">
                {({ field, form }) => (
                  <FormControl isInvalid={form.errors.price && form.touched.price}>
                    <FormLabel htmlFor="price">Price</FormLabel>
                    <Input
                      {...field}
                      id="price"
                      type="number"
                      borderRadius="16px"
                    />
                    <FormErrorMessage>{form.errors.price}</FormErrorMessage>
                  </FormControl>
                )}
              </Field>

              <Field name="transactionDate">
                {({ field, form }) => (
                  <FormControl isInvalid={form.errors.transactionDate && form.touched.transactionDate}>
                    <FormLabel htmlFor="transactionDate">Transaction Date</FormLabel>
                    <Input
                      {...field}
                      id="transactionDate"
                      type="date"
                      borderRadius="16px"
                    />
                    <FormErrorMessage>{form.errors.transactionDate}</FormErrorMessage>
                  </FormControl>
                )}
              </Field>

              <Field name="tenure">
                {({ field, form }) => (
                  <FormControl isInvalid={form.errors.tenure && form.touched.tenure}>
                    <FormLabel htmlFor="tenure">Tenure</FormLabel>
                    <Input
                      {...field}
                      id="tenure"
                      type="number"
                      borderRadius="16px"
                    />
                    <FormErrorMessage>{form.errors.tenure}</FormErrorMessage>
                  </FormControl>
                )}
              </Field>

              <Field name="resale">
                {({ field, form }) => (
                  <FormControl isInvalid={form.errors.resale && form.touched.resale}>
                    <FormLabel htmlFor="resale">Resale</FormLabel>
                    <Input
                      {...field}
                      id="resale"
                      placeholder="Resale / Private"
                      borderRadius="16px"
                    />
                    <FormErrorMessage>{form.errors.resale}</FormErrorMessage>
                  </FormControl>
                )}
              </Field>

              <Button
                mt={4}
                colorScheme="brand"
                // isLoading={props.isSubmitting}
                type="submit">
                Submit
              </Button>
            </Form>
          )}

        </Formik>

      </SimpleGrid>
    </Box>


    // <Box pt={{ base: "130px", md: "80px", xl: "80px" }}>
    //   <SimpleGrid
    //     columns={{ base: 1, md: 2, lg: 3, "2xl": 6 }}
    //     gap="20px"
    //     mb="20px"
    //   >
    //     <Formik
    //       initialValues={{ name: "Sasuke" }}
    //       // onSubmit={(values, actions) => {
    //       //   setTimeout(() => {
    //       //     alert(JSON.stringify(values, null, 2))
    //       //     actions.setSubmitting(false)
    //       //   }, 1000)
    //       // }}
    //     >
    //       {(props) => (
    //         <form>
    //           <Field name="name" validate={validateStreet}>
    //             {({ field, form }) => (
    //               <FormControl isInvalid={form.errors.name && form.touched.name}>
    //                 <FormLabel htmlFor="name">First name</FormLabel>
    //                 <Input
    //                   {...field}
    //                   id="name"
    //                   placeholder="name"
    //                   borderRadius="16px"
    //                 />
    //                 <FormErrorMessage>{form.errors.name}</FormErrorMessage>
    //               </FormControl>
    //             )}
    //           </Field>

    //           <Field name="name" validate={validateStreet}>
    //             {({ field, form }) => (
    //               <FormControl isInvalid={form.errors.name && form.touched.name}>
    //                 <FormLabel htmlFor="name">First name</FormLabel>
    //                 <Input
    //                   {...field}
    //                   id="name"
    //                   placeholder="name"
    //                   borderRadius="16px"
    //                 />
    //                 <FormErrorMessage>{form.errors.name}</FormErrorMessage>
    //               </FormControl>
    //             )}
    //           </Field>

    //           <Button
    //             mt={4}
    //             colorScheme="brand"
    //             isLoading={props.isSubmitting}
    //             type="submit"
    //           >
    //             Submit
    //           </Button>
    //         </form>
    //       )}
    //     </Formik>
    //   </SimpleGrid>
    // </Box>




  );
};

export default TransactionForm;
