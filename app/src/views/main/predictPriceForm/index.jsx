import { Field, Formik, Form } from "formik";
import * as Yup from "yup"
import {
    Box,
    Button,
    FormControl,
    FormLabel,
    FormErrorMessage,
    Input,
    SimpleGrid
} from "@chakra-ui/react"

import axios from "axios";

const PredictivePriceForm = (props) => {
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
        axios.post('http://localhost:5000/predictpropertyprice', {
            values
        })
            .then((response) => {
                console.log(response);
            }, (error) => {
                console.log(error);
            });
    }

    const validationSchema = Yup.object({
        street: Yup.string().required("Street is required!"),
        floor: Yup.number()
            .min(0, "Floor level cannot be negative")
            .required("Floor level is required!"),
        district: Yup.number()
            .min(1, "District must be larger than 0")
            .max(28, "Singapore only has 28 districts")
            .required("District is required!"),
        area: Yup.number()
            .positive("Area must be positive")
            .required("Area is required!"),
        transactionDate: Yup.date()
            .min(new Date(), "Property should not be sold yet"),
        resale: Yup.mixed()
            .oneOf(["private", "resale"], "Has to be either resale or private")
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
                >
                    {(props) => (
                        <Form action='http://localhost:5000/addpropertytransaction' method="post">
                            <Field name="street">
                                {({ field, form }) => (
                                    <FormControl isInvalid={form.errors.street && form.touched.street}>
                                        <FormLabel htmlFor="street">Street Name</FormLabel>
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

                            <Field name="transactionDate">
                                {({ field, form }) => (
                                    <FormControl isInvalid={form.errors.transactionDate && form.touched.transactionDate}>
                                        <FormLabel htmlFor="transactionDate">Future Transaction Date</FormLabel>
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
    );
};

export default PredictivePriceForm;
